import tkinter as tk
from serial import Serial

SERIAL_PORT = "/dev/ttyV0"  # socat PTY
BAUDRATE = 9600
SEND_INTERVAL_MS = 1
SYNC = 0xAA


class ControlPanel(tk.Frame):
    def __init__(self, master, controller_id):
        super().__init__(master, borderwidth=2, relief="groove")
        self.controller_id = controller_id

        tk.Label(self, text=f"Controller {controller_id}").pack()

        self.sliders = []
        for i in range(3):
            s = tk.Scale(self, from_=0, to=255, orient="horizontal")
            s.pack(fill="x")
            self.sliders.append(s)

        self.button_state = tk.IntVar(value=0)
        self.button = tk.Checkbutton(
            self, text="Button", variable=self.button_state
        )
        self.button.pack()

    def get_controls(self):
        return {
            0: self.sliders[0].get(),
            1: self.sliders[1].get(),
            2: self.sliders[2].get(),
            3: self.button_state.get(),
        }


class MockDevice:
    def __init__(self, root):
        self.root = root
        self.serial = Serial(SERIAL_PORT, BAUDRATE, timeout=0)

        self.panels = []
        self.last_states = []  # Track last sent state
        for i in range(4):
            panel = ControlPanel(root, i)
            panel.pack(side="left", padx=5, pady=5)
            self.panels.append(panel)
            self.last_states.append({})  # empty dict initially

        self.schedule_send()

    def schedule_send(self):
        self.send_all()
        self.root.after(SEND_INTERVAL_MS, self.schedule_send)

    def send_all(self):
        for i, panel in enumerate(self.panels):
            current = panel.get_controls()
            if current != self.last_states[i]:
                # State changed, send packet
                packet = self.build_packet(panel)
                self.serial.write(packet)
                self.last_states[i] = current.copy()  # update last sent

    def build_packet(self, panel):
        controls = panel.get_controls()
        packet = bytearray()

        packet.append(SYNC)
        packet.append(panel.controller_id)
        packet.append(len(controls))

        for cid, val in controls.items():
            packet.append(cid)
            packet.append(val)

        return bytes(packet)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Mock Controller Device")
    MockDevice(root)
    root.mainloop()
