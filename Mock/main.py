
import tkinter as tk
from serial import Serial

SERIAL_PORT = "/tmp/ttyV0"   # socat PTY
BAUDRATE = 9600
SEND_INTERVAL_MS = 50
SYNC = 0xAA
MSG = 0x00
MSG_RESET = 0x01
CONTROLLER_ALL = 0xFF


class ControlPanel(tk.Frame):
    def __init__(self, master, controller_id, slider_vars, button_cb):
        super().__init__(master, borderwidth=2, relief="groove")
        self.controller_id = controller_id
        self.slider_vars = slider_vars
        self.button_cb = button_cb

        tk.Label(self, text=f"Controller {controller_id}").pack()

        # Shared sliders
        self.sliders = []
        for i in range(3):
            s = tk.Scale(
                self,
                from_=0,
                to=255,
                orient="horizontal",
                variable=self.slider_vars[i],
                resolution=1,
                showvalue=True
            )
            s.pack(fill="x")
            self.sliders.append(s)

        # Per-controller button
        self.button_state = tk.IntVar(value=0)
        self.button = tk.Checkbutton(
            self,
            text="Confirm",
            variable=self.button_state,
            command=self.on_button
        )
        self.button.pack()

    def on_button(self):
        self.button_cb(self.controller_id, self.button_state.get())

    def get_controls(self):
        return {
            0: self.slider_vars[0].get(),
            1: self.slider_vars[1].get(),
            2: self.slider_vars[2].get(),
            3: self.button_state.get(),
        }

    def reset(self):
        # Reset sliders
        for var in self.slider_vars:
            var.set(0)

        # Reset button
        self.button_state.set(0)

    def reset_controller(self, cid):
        print(f"RESET CONTROLLER {cid}")
        self.controllers.pop(cid, None)
        self.redraw_ui()


class MockDevice:
    def __init__(self, root):
        self.root = root
        self.serial = Serial(SERIAL_PORT, BAUDRATE, timeout=0)

        # Shared slider state (single source of truth)
        self.slider_vars = [tk.IntVar(value=0) for _ in range(3)]

        # Trace changes without needing an index
        for var in self.slider_vars:
            var.trace_add("write", lambda *_: self.on_slider_change())

        self.panels = {}
        self.last_states = []
        self.consensus_invalidated = False
        self.rx_buffer = bytearray()

        for i in range(4):
            panel = ControlPanel(
                root,
                i,
                self.slider_vars,
                self.button_pressed
            )
            panel.pack(side="left", padx=5, pady=5)
            self.panels[i] = panel
            self.last_states.append({})

        self.schedule_send()
        self.schedule_read()

    def on_slider_change(self):
        self.consensus_invalidated = True

    def button_pressed(self, controller_id, state):
        panel = self.panels[controller_id]
        packet = self.build_packet(panel)
        self.serial.write(packet)
        self.last_states[controller_id] = panel.get_controls().copy()

    def schedule_send(self):
        self.send_all()
        self.root.after(SEND_INTERVAL_MS, self.schedule_send)

    def schedule_read(self):
        try:
            data = self.serial.read(self.serial.in_waiting or 1)
            # print(data)
            if data:
                self.rx_buffer.extend(data)
        except Exception as e:
            print("Serial error:", e)
            return

        while True:
            controller_id = self.parse_reset(self.rx_buffer)
            if controller_id is None:
                break

            self.handle_reset(controller_id)

        self.root.after(10, self.schedule_read)

    def handle_reset(self, controller_id):
        if controller_id == 0xFF:
            for controller_id in self.panels:
                self.reset_controller(controller_id)
        else:
            self.reset_controller(controller_id)

    def reset_controller(self, cid):
        print(f"RESET CONTROLLER {cid}")
        panel = self.panels.get(cid)
        if panel:
            panel.reset()

    def parse_reset(self, buffer: bytearray):
        i = 0

        while i <= len(buffer) - 4:
            if buffer[i] != SYNC:
                i += 1
                continue

            msg_type = buffer[i + 1]

            # Only care about RESET for now
            if msg_type != MSG_RESET:
                i += 1
                continue

            controller_id = buffer[i + 2]

            # Reset packet is always 4 bytes
            del buffer[i:i + 4]

            return controller_id

        return None

    def send_all(self):
        for i in self.panels:
            panel = self.panels.get(i)
            current = panel.get_controls()
            if current != self.last_states[i]:
                packet = self.build_packet(panel)
                self.serial.write(packet)
                self.last_states[i] = current.copy()

    def build_packet(self, panel):
        controls = panel.get_controls()
        packet = bytearray()

        packet.append(SYNC)
        packet.append(MSG)
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
