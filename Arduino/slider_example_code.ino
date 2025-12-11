// Motor follow potmeter (speed + direction)
// Pins (aan te passen als je andere pins wilt)
const int potPin = A0;
const int enaPin = 9;   // PWM (snelheid)
const int in1Pin = 7;   // richting
const int in2Pin = 8;   // richting

// Config
const int deadZone = 30;          // dode-zone rond midden (0..1023)
const int analogMid = 512;
const int maxPWM = 255;
const int rampStep = 3;           // hoeveel PWM per loop mag veranderen (soft-start)
const int loopDelayMs = 10;       // vertraging per loop

int currentPWM = 0;

void setup() {
  pinMode(enaPin, OUTPUT);
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);

  digitalWrite(in1Pin, LOW);
  digitalWrite(in2Pin, LOW);
  analogWrite(enaPin, 0);
}

void loop() {
  int pot = analogRead(potPin);   // 0 - 1023

  int diff = pot - analogMid;

  // dode-zone
  if (abs(diff) <= deadZone) {
    // stop: beide richtingpinnen LOW (vrijlopen) of beide HIGH (rem) — hier vrijlopen
    digitalWrite(in1Pin, LOW);
    digitalWrite(in2Pin, LOW);
    rampTo(0);
  } else {
    // bepaal richting
    if (diff > 0) {
      digitalWrite(in1Pin, HIGH);
      digitalWrite(in2Pin, LOW);
    } else {
      digitalWrite(in1Pin, LOW);
      digitalWrite(in2Pin, HIGH);
    }

    // snelheid: schaal |diff| (0..511-deadZone) naar 0..maxPWM
    int maxDiff = 511 - deadZone;
    int speed = map(min(abs(diff), maxDiff), 0, maxDiff, 0, maxPWM);
    rampTo(speed);
  }

  delay(loopDelayMs);
}

void rampTo(int target) {
  if (currentPWM < target) {
    currentPWM = min(currentPWM + rampStep, target);
  } else if (currentPWM > target) {
    currentPWM = max(currentPWM - rampStep, target);
  }
  analogWrite(enaPin, currentPWM);
}
