from serial import Serial

SYNC = 0xAA
MSG_RESET = 0x01
CONTROLLER_ALL = 0xFF


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
            print(result)
            return controller_id, controls, packet_len

    def send_reset(self):
        self.send_packet_stream(0x01, 0xFF)

    def send_packet_stream(self, msg, val):
        # TODO fix length
        self.serial.write(self.build_packet_stream(msg, val, 1))

    def build_packet_stream(self, msg, val, len):
        packet = bytearray()
        packet.append(SYNC)
        packet.append(msg)
        packet.append(val)
        packet.append(len)

        return packet

    def decode_packet_stream(self, buffer: bytearray):
        i = 0
        # need at least SYNC+msg_type+Controller+Count to start reading the buffer
        while i <= len(buffer) - 2:
            if buffer[i] != SYNC:
                i += 1
                continue

            # Potential packet header found
            msg_type = buffer[i + 1]
            controller_id = buffer[i + 2]
            count = buffer[i + 3]

            if msg_type == 0x00:
                packet_len = 4 + count * 2  # full packet length

                if i + packet_len > len(buffer):
                    break

                controls = {}
                offset = i + 4
                for _ in range(count):
                    cid = buffer[offset]
                    val = buffer[offset + 1]
                    controls[cid] = val
                    offset += 2

                # Remove packet from buffer
                del buffer[i:i + packet_len]

                return controller_id, controls, packet_len
            if msg_type == 0x01:
                ...

        # No full packet found, remove bytes before next possible SYNC
        del buffer[:i]
        return None
