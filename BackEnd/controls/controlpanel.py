from designpatterns.observer import Observable
from controls.button import Button
from controls.slider import Slider


class ControlPanel(Observable):
    # ControlPanel(1, [1,2], 3)
    def __init__(self, control_panel_id, slider_ids, button_id):
        super().__init__()
        self.sliders = self.initialize_slider(slider_ids)
        self.button = Button(button_id)
        self.button.subscribe(self.ButtonHandler)

    def SubscribeButton(self, clb):
        self.button.subscribe(clb)

    def SubscribeSliders(self, clb):
        for slider in self.sliders:
            slider.subscribe(clb)

    def getSliders(self):
        return self.sliders

    def ButtonHandler(self, event):
        # handle button updates within control panel
        ...

    def SliderHandler(self, event):
        # handle slider updates within control panel
        ...

    def initialize_slider(self, slider_ids):
        sliders = []
        for id in slider_ids:
            slider = Slider(id)
            slider.subscribe(self.SliderHandler)
            sliders.append(slider)

        return sliders
