#include <Arduino.h>

/* -------------------- CONFIG -------------------- */

#define DEADZONE 20
#define PWM_MAX 170
#define PWM_MIN 50
#define HAND_THRESHOLD 5
#define STABLE_TIME_MS 1000
#define LPF_ALPHA 0.2

#define ENDSTOP_TIMEOUT_CAL 2000
#define ENDSTOP_TIMEOUT_RUN 800
#define MIN_MOVEMENT 2

#define SYNC 0xAA
#define MSG  0x00
#define MSG_RESET 0x01

#define SLIDERS_PER_PANEL 3

/* -------------------- STRUCTS -------------------- */

struct Controls {
  uint8_t id;
  uint8_t slider[SLIDERS_PER_PANEL];
  bool button;
};

struct Slider {
  uint8_t pot_pin;
  uint8_t in_1;
  uint8_t in_2;
  uint8_t pwm;
  uint8_t stby;

  volatile uint8_t *in1_out;
  volatile uint8_t *in1_dir;
  uint8_t in1_bit;

  volatile uint8_t *in2_out;
  volatile uint8_t *in2_dir;
  uint8_t in2_bit;

  volatile uint8_t *stby_out;
  volatile uint8_t *stby_dir;
  uint8_t stby_bit;

  int lastRaw;
  float posFiltered;

  bool active;
  uint16_t last_pos;
  uint32_t time;
};

/* -------------------- SLIDERS -------------------- */

Slider sliders[] = {
  {A0, 22, 23, 5, 24},
  {A1, 26, 27, 6, 24},
  {A2, 28, 29, 7, 25},
  {A3, 30, 31, 8, 25},
};

const uint8_t NUM_SLIDERS = sizeof(sliders) / sizeof(sliders[0]);

/* -------------------- CONTROL PANEL -------------------- */

Controls panel1 = {1, {0, 0, 0}, false};
Controls last_sent = {0, {255, 255, 255}, true};

unsigned long last_update = 0;
const unsigned long UPDATE_INTERVAL = 1000;

/* -------------------- PROTOTYPES -------------------- */

float lowPassFilter(int raw, float prev);
void initPin(uint8_t pin, volatile uint8_t **out, volatile uint8_t **dir, uint8_t *bit);
void initSlider(Slider &s);
void driveMotorSafe(Slider &s, int current, int target);
void calibrateAll();

uint8_t sliderToByte(const Slider &s);
void updateControlsFromSliders();

bool hasChanged(const Controls& current, const Controls& last);
void copyControls(const Controls& src, Controls& dest);
uint8_t* createPacket(const Controls& ctrl, uint8_t& packet_len);
void sendControlPacket(const Controls& ctrl);

/* -------------------- UTILS -------------------- */

float lowPassFilter(int raw, float prev) {
  return LPF_ALPHA * raw + (1.0f - LPF_ALPHA) * prev;
}

void initPin(uint8_t pin, volatile uint8_t **out,
             volatile uint8_t **dir, uint8_t *bit) {
  uint8_t port = digitalPinToPort(pin);
  *out = portOutputRegister(port);
  *dir = portModeRegister(port);
  *bit = digitalPinToBitMask(pin);
}

void initSlider(Slider &s) {
  initPin(s.in_1, &s.in1_out, &s.in1_dir, &s.in1_bit);
  initPin(s.in_2, &s.in2_out, &s.in2_dir, &s.in2_bit);
  initPin(s.stby, &s.stby_out, &s.stby_dir, &s.stby_bit);

  *s.in1_dir  |= s.in1_bit;
  *s.in2_dir  |= s.in2_bit;
  *s.stby_dir |= s.stby_bit;
  *s.stby_out |= s.stby_bit;
}

/* -------------------- MOTOR -------------------- */

void driveMotorSafe(Slider &s, int current, int target) {
  int diff = target - current;

  if (abs(diff) <= DEADZONE) {
    analogWrite(s.pwm, 0);
    s.active = false;
    s.time = millis();
    s.last_pos = current;
    return;
  }

  if (abs(current - s.last_pos) < MIN_MOVEMENT) {
    if (millis() - s.time > ENDSTOP_TIMEOUT_RUN) {
      analogWrite(s.pwm, 0);
      s.active = false;
      return;
    }
  } else {
    s.time = millis();
    s.last_pos = current;
  }

  s.active = true;

  if (diff > 0) {
    *s.in1_out |=  s.in1_bit;
    *s.in2_out &= ~s.in2_bit;
  } else {
    *s.in1_out &= ~s.in1_bit;
    *s.in2_out |=  s.in2_bit;
  }

  int pwm = map(abs(diff), DEADZONE, 1023, PWM_MIN, PWM_MAX);
  analogWrite(s.pwm, constrain(pwm, PWM_MIN, PWM_MAX));
}

/* -------------------- CONTROLS -------------------- */

uint8_t sliderToByte(const Slider &s) {
  return map((int)s.posFiltered, 0, 1023, 0, 255);
}

void updateControlsFromSliders() {
  for (uint8_t i = 0; i < SLIDERS_PER_PANEL && i < NUM_SLIDERS; i++) {
    panel1.slider[i] = sliderToByte(sliders[i]);
  }
  panel1.button = false;
}

bool hasChanged(const Controls& current, const Controls& last) {
  if (current.id != last.id) return true;
  for (uint8_t i = 0; i < SLIDERS_PER_PANEL; i++) {
    if (current.slider[i] != last.slider[i]) return true;
  }
  return current.button != last.button;
}

void copyControls(const Controls& src, Controls& dest) {
  dest = src;
}

uint8_t* createPacket(const Controls& ctrl, uint8_t& packet_len) {
  const uint8_t control_count = SLIDERS_PER_PANEL + 1;
  packet_len = 4 + control_count * 2;

  static uint8_t packet[32];
  uint8_t i = 0;

  packet[i++] = SYNC;
  packet[i++] = MSG;
  packet[i++] = ctrl.id;
  packet[i++] = control_count;

  for (uint8_t s = 0; s < SLIDERS_PER_PANEL; s++) {
    packet[i++] = s;
    packet[i++] = ctrl.slider[s];
  }

  packet[i++] = SLIDERS_PER_PANEL;
  packet[i++] = ctrl.button ? 1 : 0;

  return packet;
}

void sendControlPacket(const Controls& ctrl) {
  uint8_t len;
  uint8_t* pkt = createPacket(ctrl, len);
  Serial.write(pkt, len);
}

/* -------------------- CALIBRATION -------------------- */

void calibrateAll() {
  unsigned long start = millis();

  while (millis() - start < ENDSTOP_TIMEOUT_CAL) {
    bool done = true;
    for (uint8_t i = 0; i < NUM_SLIDERS; i++) {
      int raw = analogRead(sliders[i].pot_pin);
      if (raw < 1000) {
        driveMotorSafe(sliders[i], raw, 1023);
        done = false;
      }
    }
    if (done) break;
    delay(20);
  }

  start = millis();
  while (millis() - start < ENDSTOP_TIMEOUT_CAL) {
    bool done = true;
    for (uint8_t i = 0; i < NUM_SLIDERS; i++) {
      int raw = analogRead(sliders[i].pot_pin);
      if (raw > 20) {
        driveMotorSafe(sliders[i], raw, 0);
        done = false;
      }
    }
    if (done) break;
    delay(20);
  }

  for (uint8_t i = 0; i < NUM_SLIDERS; i++) {
    analogWrite(sliders[i].pwm, 0);
    sliders[i].active = false;
  }
}

/* -------------------- SETUP -------------------- */

void setup() {
  Serial.begin(9600);

  for (uint8_t i = 0; i < NUM_SLIDERS; i++) {
    Slider &s = sliders[i];
    initSlider(s);
    s.lastRaw = analogRead(s.pot_pin);
    s.posFiltered = s.lastRaw;
    s.last_pos = s.lastRaw;
    s.active = false;
    s.time = millis();
  }

  calibrateAll();
}

/* -------------------- LOOP -------------------- */

void loop() {
  unsigned long now = millis();
  int master = -1;

  for (uint8_t i = 0; i < NUM_SLIDERS; i++) {
    Slider &s = sliders[i];
    int raw = analogRead(s.pot_pin);

    s.posFiltered = lowPassFilter(raw, s.posFiltered);

    if (!s.active && abs(raw - s.lastRaw) > HAND_THRESHOLD && master < 0) {
      master = i;
    }

    s.lastRaw = raw;
  }

  if (master >= 0) {
    int target = sliders[master].posFiltered;
    for (uint8_t i = 0; i < NUM_SLIDERS; i++) {
      if (i != master)
        driveMotorSafe(sliders[i], sliders[i].posFiltered, target);
      else
        analogWrite(sliders[i].pwm, 0);
    }
  }

  updateControlsFromSliders();

  if (now - last_update >= UPDATE_INTERVAL) {
    last_update = now;
    if (hasChanged(panel1, last_sent)) {
      sendControlPacket(panel1);
      copyControls(panel1, last_sent);
    }
  }

  delay(20);
}
