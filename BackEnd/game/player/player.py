from game.player.playercontrols import PlayerControls


class Player:
    def __init__(self, controls):
        self.controls = PlayerControls(controls)

    def getSliderData(self):
        return self.controls.slidersState

    def Agree(self, question):
        if self.controls.buttonState:
            # save shit...
            return True
