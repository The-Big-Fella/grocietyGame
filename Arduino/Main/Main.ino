#define SYNC 0xAA
#define MSG 0x00
#define MSG_RESET 0x01

struct Controls {
  uint8_t id;
  uint8_t slider[3];
  bool button;
};

struct ControlPanel {
  Controls panels[4];
};

Controls panel1 = {1, {50, 50, 50}, 0};

Controls last_sent = {0, {255, 255, 255}, true}; // impossible initial values

unsigned long last_update = 0; // track time
const unsigned long UPDATE_INTERVAL = 1000; // 1 second

void setup() {
  Serial.begin(9600);
  delay(1000);
}

void loop() {
  unsigned long now = millis();

  // Update sliders every second
  if (now - last_update >= UPDATE_INTERVAL) {
    last_update = now;

    // Example: increment sliders by 1, wrap around 0–255
    for (uint8_t i = 0; i < 3; i++) {
      panel1.slider[i] = (panel1.slider[i] + 1) % 256;
    }
  }

  // Send packet only if changed
  if (hasChanged(panel1, last_sent)) {
    sendControlPacket(panel1);
    copyControls(panel1, last_sent);
  }
}

// Check if current state differs from last sent
bool hasChanged(const Controls& current, const Controls& last) {
  if (current.id != last.id) return true;
  for (uint8_t i = 0; i < 3; i++) {
    if (current.slider[i] != last.slider[i]) return true;
  }
  if (current.button != last.button) return true;
  return false;
}

// Copy current state to last_sent
void copyControls(const Controls& src, Controls& dest) {
  dest.id = src.id;
  for (uint8_t i = 0; i < 3; i++) {
    dest.slider[i] = src.slider[i];
  }
  dest.button = src.button;
}

// Create packet from Controls
uint8_t* createPacket(const Controls& ctrl, uint8_t& packet_len) {
  const uint8_t control_count = 4; // 3 sliders + button
  packet_len = 4 + control_count * 2;

  static uint8_t packet[12];
  uint8_t index = 0;

  packet[index++] = SYNC;
  packet[index++] = MSG;
  packet[index++] = ctrl.id;
  packet[index++] = control_count;

  // Add sliders
  for (uint8_t i = 0; i < 3; i++) {
    packet[index++] = i;
    packet[index++] = ctrl.slider[i];
  }

  // Add button
  packet[index++] = 3;
  packet[index++] = ctrl.button ? 1 : 0;

  return packet;
}

// Send packet
void sendControlPacket(const Controls& ctrl) {
  uint8_t packet_len;
  uint8_t* packet = createPacket(ctrl, packet_len);

  Serial.write(packet, packet_len);
  Serial.flush();

  // Debug
  Serial.print("Packet sent: ");
  for (uint8_t i = 0; i < packet_len; i++) {
    Serial.print(packet[i], HEX);
    Serial.print(" ");
  }
  Serial.println();
}

