from designpaterns.observer import Observer


class PlayerControls(Observer):
    # Controller (1,2,3 of 4)
    def __init__(self, controller):
        self.controlPanel = controller

        self.controlPanel.SubscribeButton(self.handleButton)
        self.controlPanel.SubscribeSliders(self.handleSlider)

        self.buttonState = False
        self.slidersState = self.intialize_slider_state(
            self.controlPanel.getSliders())

    def handleButton(self, event):
        self.buttonState = event.get("is_pressed", False)

    def handleSlider(self, event):
        slider_id = event.get("id", None)
        if slider_id in self.slidersState.keys():
            self.slidersState[slider_id] = event.get("position")

    def intialize_slider_state(self, sliders):
        sliders_state = {}
        for slider in sliders:
            sliders_state[slider.id] = 0

        return sliders_state
