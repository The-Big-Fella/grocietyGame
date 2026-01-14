import time
# import threading
import os

from controls.translationlayer import TranslationLayer
from controls.controlpanel import ControllerManager


PORT = 5000
HOST = "0.0.0.0"
CONTROLLER = os.getenv("CONTROLLER_PATH")


class App:
    def __init__(self):
        self.io = TranslationLayer(CONTROLLER, 9600)

        self.controllers = ControllerManager(io=self.io)

    # def start_api(self):
    #    t = threading.Thread(
    #        target=lambda: self.api_server.run(
    #            host="0.0.0.0", port=5000, debug=False, use_reloader=False),
    #        daemon=True,
    #    )
    #    t.start()
    #    print("API server running on http://localhost:5000")

    def controller_update(self):
        result = self.io.update()
        if result:
            print(result)
            cid, controls, _ = result
            self.controllers.update_from_packet(cid, controls)

    def run(self):
        # self.start_api()
        # self.game.start_game()

        while True:
            self.controller_update()
            # self.game.update()
            time.sleep(0.001)


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
