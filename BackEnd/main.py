import time

from controls.translationlayer import TranslationLayer
from controls.controlpanel import ControllerManager
from game.game import Game


class App:
    def __init__(self):
        self.io = TranslationLayer("/tmp/ttyV1", 9600)

        self.controllers = ControllerManager(io=self.io)

        self.game = Game(control_manager=self.controllers)

    def controller_update(self):
        result = self.io.update()
        if result:
            cid, controls, _ = result
            self.controllers.update_from_packet(cid, controls)

    def run(self):
        self.game.start_game()

        while True:
            self.controller_update()
            self.game.update()
            time.sleep(0.001)


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
