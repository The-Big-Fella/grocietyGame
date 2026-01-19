
#include <Arduino.h>

/* =========================================================
   SERIAL PROTOCOL
   ========================================================= */
#define SYNC 0xAA
#define MSG  0x00

struct Controls {
  uint8_t id;
  uint8_t slider[3];
  bool button;
};

/* =========================================================
   PIN DEFINITIONS
   ========================================================= */
// Potmeters
#define POT1_PIN A0
#define POT2_PIN A1
#define POT3_PIN A3
#define POT4_PIN A4
#define POT5_PIN A5
#define POT6_PIN A6

// Motorfader A
#define AIN1 22
#define AIN2 23
#define PWMA 5

// Motorfader B
#define BIN1 26
#define BIN2 27
#define PWMB 6

// Motorfader C
#define CIN1 28
#define CIN2 29
#define PWMC 7

// Motorfader D
#define DIN1 32
#define DIN2 33
#define PWMD 8

// Motorfader E
#define EIN1 34
#define EIN2 35
#define PWME 9

// Motorfader F
#define FIN1 38
#define FIN2 39
#define PWMF 10

// Standby pins
#define STBY_PIN 24
#define STBY_PIN2 30
#define STBY_PIN3 36

/* =========================================================
   CONFIGURATION
   ========================================================= */
#define DEADZONE 20
#define PWM_MAX 170
#define PWM_MIN 50
#define HAND_THRESHOLD 5
#define LPF_ALPHA 0.2

const int THRESHOLD_TOP = 900;
const int THRESHOLD_BOTTOM = 100;

const unsigned long FOLLOW_INTERVAL = 20;

/* =========================================================
   VARIABLES
   ========================================================= */
unsigned long lastFollowTime = 0;

float posAFiltered = 0, posBFiltered = 0, posCFiltered = 0;
float posDFiltered = 0, posEFiltered = 0, posFFiltered = 0;

int masterSlider = 0;

/* -------- Controllers -------- */
Controls ctrl1 = {1, {0, 0, 0}, false};   // A B C
Controls ctrl2 = {2, {0, 0, 0}, false};   // D E F

Controls lastSent1 = {1, {255, 255, 255}, true};
Controls lastSent2 = {2, {255, 255, 255}, true};

/* =========================================================
   HELPER FUNCTIONS
   ========================================================= */
float lowPassFilter(int raw, float prev) {
  return LPF_ALPHA * raw + (1.0 - LPF_ALPHA) * prev;
}

void driveMotor(int current, int target, int pinA, int pinB, int pwmPin, bool inverted = false) {
  int diff = target - current;

  if (abs(diff) <= DEADZONE) {
    analogWrite(pwmPin, 0);
    return;
  }

  bool forward = diff > 0;
  if (inverted) forward = !forward;

  digitalWrite(pinA, forward ? HIGH : LOW);
  digitalWrite(pinB, forward ? LOW : HIGH);

  int pwm = map(abs(diff), DEADZONE,
                THRESHOLD_TOP - THRESHOLD_BOTTOM,
                PWM_MIN, PWM_MAX);

  pwm = constrain(pwm, PWM_MIN, PWM_MAX);
  analogWrite(pwmPin, pwm);
}

/* =========================================================
   PACKET FUNCTIONS
   ========================================================= */
bool hasChanged(const Controls& a, const Controls& b) {
  for (uint8_t i = 0; i < 3; i++) {
    if (a.slider[i] != b.slider[i]) return true;
  }
  return a.button != b.button;
}

void copyControls(const Controls& src, Controls& dst) {
  for (uint8_t i = 0; i < 3; i++) dst.slider[i] = src.slider[i];
  dst.button = src.button;
}

uint8_t* createPacket(const Controls& ctrl, uint8_t& len) {
  static uint8_t packet[12];
  uint8_t idx = 0;

  packet[idx++] = SYNC;
  packet[idx++] = MSG;
  packet[idx++] = ctrl.id;
  packet[idx++] = 4; // 3 sliders + button

  for (uint8_t i = 0; i < 3; i++) {
    packet[idx++] = i;
    packet[idx++] = ctrl.slider[i];
  }

  packet[idx++] = 3;
  packet[idx++] = ctrl.button ? 1 : 0;

  len = idx;
  return packet;
}

void sendControlPacket(const Controls& ctrl) {
  uint8_t len;
  uint8_t* p = createPacket(ctrl, len);
  Serial.write(p, len);
}

/* =========================================================
   SETUP
   ========================================================= */
void setup() {
  pinMode(AIN1, OUTPUT); pinMode(AIN2, OUTPUT); pinMode(PWMA, OUTPUT);
  pinMode(BIN1, OUTPUT); pinMode(BIN2, OUTPUT); pinMode(PWMB, OUTPUT);
  pinMode(CIN1, OUTPUT); pinMode(CIN2, OUTPUT); pinMode(PWMC, OUTPUT);
  pinMode(DIN1, OUTPUT); pinMode(DIN2, OUTPUT); pinMode(PWMD, OUTPUT);
  pinMode(EIN1, OUTPUT); pinMode(EIN2, OUTPUT); pinMode(PWME, OUTPUT);
  pinMode(FIN1, OUTPUT); pinMode(FIN2, OUTPUT); pinMode(PWMF, OUTPUT);

  pinMode(STBY_PIN, OUTPUT);
  pinMode(STBY_PIN2, OUTPUT);
  pinMode(STBY_PIN3, OUTPUT);

  digitalWrite(STBY_PIN, HIGH);
  digitalWrite(STBY_PIN2, HIGH);
  digitalWrite(STBY_PIN3, HIGH);

  Serial.begin(9600);

  posAFiltered = analogRead(POT1_PIN);
  posBFiltered = analogRead(POT2_PIN);
  posCFiltered = analogRead(POT3_PIN);
  posDFiltered = analogRead(POT4_PIN);
  posEFiltered = analogRead(POT5_PIN);
  posFFiltered = analogRead(POT6_PIN);
}

/* =========================================================
   LOOP
   ========================================================= */
void loop() {
  unsigned long now = millis();

  int rawA = constrain(analogRead(POT1_PIN), THRESHOLD_BOTTOM, THRESHOLD_TOP);
  int rawB = constrain(analogRead(POT2_PIN), THRESHOLD_BOTTOM, THRESHOLD_TOP);
  int rawC = constrain(analogRead(POT3_PIN), THRESHOLD_BOTTOM, THRESHOLD_TOP);
  int rawD = constrain(analogRead(POT4_PIN), THRESHOLD_BOTTOM, THRESHOLD_TOP);
  int rawE = constrain(analogRead(POT5_PIN), THRESHOLD_BOTTOM, THRESHOLD_TOP);
  int rawF = constrain(analogRead(POT6_PIN), THRESHOLD_BOTTOM, THRESHOLD_TOP);

  /* ---- Hand detection ---- */
  bool humanMoveA = abs(rawA - posAFiltered) > HAND_THRESHOLD;
  bool humanMoveB = abs(rawB - posBFiltered) > HAND_THRESHOLD;
  bool humanMoveC = abs(rawC - posCFiltered) > HAND_THRESHOLD;
  bool humanMoveD = abs(rawD - posDFiltered) > HAND_THRESHOLD;
  bool humanMoveE = abs(rawE - posEFiltered) > HAND_THRESHOLD;
  bool humanMoveF = abs(rawF - posFFiltered) > HAND_THRESHOLD;

  /* ---- Master selection ---- */
  if (humanMoveA && !humanMoveB && !humanMoveC && !humanMoveD && !humanMoveE && !humanMoveF) masterSlider = 1;
  else if (humanMoveB && !humanMoveA && !humanMoveC && !humanMoveD && !humanMoveE && !humanMoveF) masterSlider = 2;
  else if (humanMoveC && !humanMoveA && !humanMoveB && !humanMoveD && !humanMoveE && !humanMoveF) masterSlider = 3;
  else if (humanMoveD && !humanMoveA && !humanMoveB && !humanMoveC && !humanMoveE && !humanMoveF) masterSlider = 4;
  else if (humanMoveE && !humanMoveA && !humanMoveB && !humanMoveC && !humanMoveD && !humanMoveF) masterSlider = 5;
  else if (humanMoveF && !humanMoveA && !humanMoveB && !humanMoveC && !humanMoveD && !humanMoveE) masterSlider = 6;

  /* ---- Filtering ---- */
  posAFiltered = lowPassFilter(rawA, posAFiltered);
  posBFiltered = lowPassFilter(rawB, posBFiltered);
  posCFiltered = lowPassFilter(rawC, posCFiltered);
  posDFiltered = lowPassFilter(rawD, posDFiltered);
  posEFiltered = lowPassFilter(rawE, posEFiltered);
  posFFiltered = lowPassFilter(rawF, posFFiltered);

  /* ---- Motor follow logic ---- */
  if (now - lastFollowTime >= FOLLOW_INTERVAL) {
    lastFollowTime = now;

    switch (masterSlider) {
      case 1:
        driveMotor(posBFiltered, rawA, BIN1, BIN2, PWMB, true);
        driveMotor(posCFiltered, rawA, CIN1, CIN2, PWMC, true);
        driveMotor(posDFiltered, rawA, DIN1, DIN2, PWMD, true);
        driveMotor(posEFiltered, rawA, EIN1, EIN2, PWME, true);
        driveMotor(posFFiltered, rawA, FIN1, FIN2, PWMF, true);
        analogWrite(PWMA, 0);
        break;

      case 2:
        driveMotor(posAFiltered, rawB, AIN1, AIN2, PWMA, true);
        driveMotor(posCFiltered, rawB, CIN1, CIN2, PWMC, true);
        driveMotor(posDFiltered, rawB, DIN1, DIN2, PWMD, true);
        driveMotor(posEFiltered, rawB, EIN1, EIN2, PWME, true);
        driveMotor(posFFiltered, rawB, FIN1, FIN2, PWMF, true);
        analogWrite(PWMB, 0);
        break;

      case 3:
        driveMotor(posAFiltered, rawC, AIN1, AIN2, PWMA, true);
        driveMotor(posBFiltered, rawC, BIN1, BIN2, PWMB, true);
        driveMotor(posDFiltered, rawC, DIN1, DIN2, PWMD, true);
        driveMotor(posEFiltered, rawC, EIN1, EIN2, PWME, true);
        driveMotor(posFFiltered, rawC, FIN1, FIN2, PWMF, true);
        analogWrite(PWMC, 0);
        break;

      case 4:
        driveMotor(posAFiltered, rawD, AIN1, AIN2, PWMA, true);
        driveMotor(posBFiltered, rawD, BIN1, BIN2, PWMB, true);
        driveMotor(posCFiltered, rawD, CIN1, CIN2, PWMC, true);
        driveMotor(posEFiltered, rawD, EIN1, EIN2, PWME, true);
        driveMotor(posFFiltered, rawD, FIN1, FIN2, PWMF, true);
        analogWrite(PWMD, 0);
        break;

      case 5:
        driveMotor(posAFiltered, rawE, AIN1, AIN2, PWMA, true);
        driveMotor(posBFiltered, rawE, BIN1, BIN2, PWMB, true);
        driveMotor(posCFiltered, rawE, CIN1, CIN2, PWMC, true);
        driveMotor(posDFiltered, rawE, DIN1, DIN2, PWMD, true);
        driveMotor(posFFiltered, rawE, FIN1, FIN2, PWMF, true);
        analogWrite(PWME, 0);
        break;

      case 6:
        driveMotor(posAFiltered, rawF, AIN1, AIN2, PWMA, true);
        driveMotor(posBFiltered, rawF, BIN1, BIN2, PWMB, true);
        driveMotor(posCFiltered, rawF, CIN1, CIN2, PWMC, true);
        driveMotor(posDFiltered, rawF, DIN1, DIN2, PWMD, true);
        driveMotor(posEFiltered, rawF, EIN1, EIN2, PWME, true);
        analogWrite(PWMF, 0);
        break;

      default:
        analogWrite(PWMA, 0);
        analogWrite(PWMB, 0);
        analogWrite(PWMC, 0);
        analogWrite(PWMD, 0);
        analogWrite(PWME, 0);
        analogWrite(PWMF, 0);
        break;
    }
  }

  /* ---- Controller mapping ---- */
  ctrl1.slider[0] = map(rawA, THRESHOLD_BOTTOM, THRESHOLD_TOP, 0, 255);
  ctrl1.slider[1] = map(rawB, THRESHOLD_BOTTOM, THRESHOLD_TOP, 0, 255);
  ctrl1.slider[2] = map(rawC, THRESHOLD_BOTTOM, THRESHOLD_TOP, 0, 255);

  ctrl2.slider[0] = map(rawD, THRESHOLD_BOTTOM, THRESHOLD_TOP, 0, 255);
  ctrl2.slider[1] = map(rawE, THRESHOLD_BOTTOM, THRESHOLD_TOP, 0, 255);
  ctrl2.slider[2] = map(rawF, THRESHOLD_BOTTOM, THRESHOLD_TOP, 0, 255);

  /* ---- Send packets on change ---- */
  if (hasChanged(ctrl1, lastSent1)) {
    sendControlPacket(ctrl1);
    copyControls(ctrl1, lastSent1);
  }

  if (hasChanged(ctrl2, lastSent2)) {
    sendControlPacket(ctrl2);
    copyControls(ctrl2, lastSent2);
  }

  delay(20);
}

