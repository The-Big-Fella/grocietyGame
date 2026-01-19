

#include <Arduino.h>

// ---------- Protocol ----------
#define SYNC       0xAA
#define MSG        0x00
#define MSG_RESET  0x01
#define CONTROLLER_ALL 0xFF

#define SLIDER_CENTER 512

// ---------- Pins ----------
#define POT1_PIN A0
#define POT2_PIN A1
#define POT3_PIN A3
#define POT4_PIN A4
#define POT5_PIN A5
#define POT6_PIN A6

#define AIN1 22
#define AIN2 23
#define PWMA 5
#define BIN1 26
#define BIN2 27
#define PWMB 6
#define CIN1 28
#define CIN2 29
#define PWMC 7
#define DIN1 32
#define DIN2 33
#define PWMD 8
#define EIN1 34
#define EIN2 35
#define PWME 9
#define FIN1 38
#define FIN2 39
#define PWMF 10

#define STBY_PIN 24
#define STBY_PIN2 30
#define STBY_PIN3 36

// ---------- Config ----------
#define DEADZONE 20
#define PWM_MAX 170
#define PWM_MIN 50
#define HAND_THRESHOLD 5
#define LPF_ALPHA 0.2

const int THRESHOLD_TOP = 900;
const int THRESHOLD_BOTTOM = 100;
const unsigned long FOLLOW_INTERVAL = 20;

// ---------- State ----------
unsigned long lastFollowTime = 0;
unsigned long startupTime = 0;

float pos[6];
int raw[6];
int target[6];

bool resetActive = true;
bool startupButtonsSent = false;

// Controller buttons
bool buttonState[2] = {0, 0};

// ---------- Serial RX ----------
uint8_t rxBuffer[8];
uint8_t rxIndex = 0;

// ---------- Helpers ----------
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

  int pwm = map(abs(diff), DEADZONE, THRESHOLD_TOP - THRESHOLD_BOTTOM, PWM_MIN, PWM_MAX);
  pwm = constrain(pwm, PWM_MIN, PWM_MAX);
  analogWrite(pwmPin, pwm);
}

// ---------- Packet send ----------
void sendButtonPacket(uint8_t controllerId, bool value) {
  uint8_t packet[8];
  uint8_t idx = 0;

  packet[idx++] = SYNC;
  packet[idx++] = MSG;
  packet[idx++] = controllerId;
  packet[idx++] = 1;      // one control
  packet[idx++] = 3;      // button id
  packet[idx++] = value ? 1 : 0;

  Serial.write(packet, idx);
}

// ---------- RESET ----------
void handleReset(uint8_t controllerId) {
  for (int i = 0; i < 6; i++) {
    target[i] = SLIDER_CENTER;
  }

  // Reset buttons
  buttonState[0] = 0;
  buttonState[1] = 0;

  sendButtonPacket(0, 0);
  sendButtonPacket(1, 0);

  resetActive = true;
}

// ---------- SERIAL PARSE ----------
void parseSerial() {
  while (Serial.available()) {
    uint8_t b = Serial.read();
    rxBuffer[rxIndex++] = b;

    if (rxIndex >= 4 &&
        rxBuffer[0] == SYNC &&
        rxBuffer[1] == MSG_RESET) {

      handleReset(rxBuffer[2]);
      rxIndex = 0;
    }

    if (rxIndex >= sizeof(rxBuffer)) rxIndex = 0;
  }
}

// ---------- SETUP ----------
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

  for (int i = 0; i < 6; i++) {
    pos[i] = SLIDER_CENTER;
    raw[i] = SLIDER_CENTER;
    target[i] = SLIDER_CENTER;
  }

  startupTime = millis();
}

// ---------- LOOP ----------
void loop() {
  parseSerial();

  // Read pots
  raw[0] = constrain(analogRead(POT1_PIN), THRESHOLD_BOTTOM, THRESHOLD_TOP);
  raw[1] = constrain(analogRead(POT2_PIN), THRESHOLD_BOTTOM, THRESHOLD_TOP);
  raw[2] = constrain(analogRead(POT3_PIN), THRESHOLD_BOTTOM, THRESHOLD_TOP);
  raw[3] = constrain(analogRead(POT4_PIN), THRESHOLD_BOTTOM, THRESHOLD_TOP);
  raw[4] = constrain(analogRead(POT5_PIN), THRESHOLD_BOTTOM, THRESHOLD_TOP);
  raw[5] = constrain(analogRead(POT6_PIN), THRESHOLD_BOTTOM, THRESHOLD_TOP);

  for (int i = 0; i < 6; i++) {
    pos[i] = lowPassFilter(raw[i], pos[i]);
  }

  // Send startup buttons after 5 seconds
  if (!startupButtonsSent && millis() - startupTime >= 5000) {
    buttonState[0] = 1;
    buttonState[1] = 1;

    sendButtonPacket(0, 1);
    sendButtonPacket(1, 1);

    startupButtonsSent = true;
  }

  if (millis() - lastFollowTime >= FOLLOW_INTERVAL) {
    lastFollowTime = millis();

    driveMotor(pos[0], target[0], AIN1, AIN2, PWMA, true);
    driveMotor(pos[1], target[1], BIN1, BIN2, PWMB, true);
    driveMotor(pos[2], target[2], CIN1, CIN2, PWMC, true);
    driveMotor(pos[3], target[3], DIN1, DIN2, PWMD, true);
    driveMotor(pos[4], target[4], EIN1, EIN2, PWME, true);
    driveMotor(pos[5], target[5], FIN1, FIN2, PWMF, true);
  }
}

