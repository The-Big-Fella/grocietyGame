from serial import Serial

SYNC = 0xAA


class TranslationLayer():
    def __init__(self, device, baudrate):
        self.device = device
        self.baudrate = baudrate
        self.serial = Serial(device, baudrate=baudrate, timeout=.01)
        self.buffer = bytearray()

    def update(self):
        self.buffer += self.serial.read(self.serial.in_waiting or 1)

        result = self.decode_packet_stream(self.buffer)
        if result:
            controller_id, controls, packet_len = result
            print("Controller:", controller_id, "Controls:", controls)
            return controller_id, controls, packet_len

    def decode_packet_stream(self, buffer: bytearray):
        i = 0
        while i <= len(buffer) - 2:  # need at least SYNC+Controller+Count
            if buffer[i] != SYNC:
                i += 1
                continue

            # Potential packet header found
            controller_id = buffer[i + 1]
            count = buffer[i + 2]
            packet_len = 3 + count * 2  # full packet length

            if i + packet_len > len(buffer):
                # Not enough data yet
                break

            # Extract controls
            controls = {}
            offset = i + 3
            for _ in range(count):
                cid = buffer[offset]
                val = buffer[offset + 1]
                controls[cid] = val
                offset += 2

            # Remove packet from buffer
            del buffer[i:i + packet_len]

            return controller_id, controls, packet_len

        # No full packet found, remove bytes before next possible SYNC
        del buffer[:i]
        return None
