from controls.slider import Slider
from controls.button import Button


class ControlPanel:
    def __init__(self, uart, panel_id):
        self.uart = uart
        self.panel_id = panel_id
        self.slider_1 = Slider(1)
        self.slider_2 = Slider(2)
        self.slider_3 = Slider(3)
        self.button = Button(1)

    def handle_message(self, key, value):
        if key == "SLDR1":
            self.slider_1.set(value)
        elif key == "SLDR2":
            self.slider_2.set(value)
        elif key == "SLDR3":
            self.slider_3.set(value)
        elif key == "BTN":
            self.button.set(value)

    def __repr__(self):
        return f"{self.slider_1}, {self.slider_2}, {self.slider_3}, {self.button}"
