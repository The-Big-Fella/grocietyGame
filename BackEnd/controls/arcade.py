from controls.controlpanel import ControlPanel


class Arcade:
    def __init__(self, uart):
        self.uart = uart
        self.current_panel = None
        self.panels = {
            "panel1": ControlPanel(uart, "panel1"),
        }

    def handle_line(self, line):
        # Panel header
        if line.endswith(":") and line[:-1] in self.panels:
            self.current_panel = self.panels[line[:-1]]
            return

        if ":" in line and self.current_panel:
            key, value = line.split(":", 1)
            self.current_panel.handle_message(key, value)

    def poll(self):
        while True:
            line = self.uart.read_line()
            if not line:
                break
            self.handle_line(line)
