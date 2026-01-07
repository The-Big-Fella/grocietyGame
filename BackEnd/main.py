import time

from controls.translationlayer import TranslationLayer
from controls.controlpanel import ControllerManager
from game.game import Game

translationlayer = TranslationLayer("/tmp/ttyV1", 9600)
manager = ControllerManager()
game = Game(manager)
game.start_game()


def main():
    running = True
    while running:
        controller_update()
        game.update()

        time.sleep(0.001)


def controller_update():
    result = translationlayer.update()

    if result:
        controller_id, controls, packet_len = result

        manager.update_from_packet(controller_id, controls)

        # c = manager.get_controller(controller_id)
        # if c:
        #    print(f"Controller {c.controller_id} sliders={
        #        c.sliders} button={c.button}")


if __name__ == "__main__":
    main()
