from serial import Serial

SYNC = 0xAA


class TranslationLayer():
    def __init__(self, device, baudrate):
        self.device = device
        self.baudrate = baudrate
        self.serial = Serial(device, baudrate=baudrate, timeout=1)
        self.buffer = bytearray()

    def update(self):
        self.buffer += self.serial.read(self.serial.in_waiting or 1)

        result = self.decode_packet_stream(self.buffer)
        if result:
            controller_id, controls, packet_len = result
            return controller_id, controls, packet_len
            # print("Controller:", controller_id, "Controls:", controls)

    def decode_packet_stream(self, buffer: bytearray):
        """
        Continuously scan the buffer for a packet starting with SYNC (0xAA).
        Returns:
            (controller_id, controls, packet_len) if a full packet is available
            None if not enough data yet
        """
        # Loop until buffer is empty or a full packet is found
        i = 0
        while i <= len(buffer) - 3:  # need at least SYNC+Controller+Count
            if buffer[i] != SYNC:
                i += 1
                continue

            # Found potential SYNC at position i
            if i + 3 > len(buffer):
                # Not enough bytes for header yet
                break

            controller_id = buffer[i + 1]
            count = buffer[i + 2]
            packet_len = 3 + count * 2  # SYNC + Controller + Count + Controls

            if i + packet_len > len(buffer):
                # Full packet not yet received
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

# No full packet found yet
# Remove all bytes before the next potential SYNC to avoid buffer bloat
        del buffer[:i]
        return None
