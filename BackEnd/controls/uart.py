import queue
import serial
import threading


class Uart:
    def __init__(self, port="/dev/serial0", baudrate=115200, timeout=0.1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.lock = threading.Lock()

    def write(self, msg: str):
        with self.lock:
            self.ser.write((msg + "\n").encode())

    def read(self):
        with self.lock:
            if self.ser.in_waiting:
                return self.ser.readline().decode().strip()
        return None


class UartMock:
    def __init__(self):
        self.rx = queue.Queue()
        self.tx = queue.Queue()

    def write(self, msg):
        print(f"[UART WRITE] {msg}")
        self.tx.put(msg)

    def read_line(self):
        try:
            return self.rx.get_nowait()
        except:
            return None
