import time
import threading
import os

from controls.translationlayer import TranslationLayer
from controls.controlpanel import ControllerManager
from game.game import Game
from api.flask import ApiServer
from database.database import Database


PORT = 5000
HOST = "0.0.0.0"
CONTROLLER = os.getenv("CONTROLLER_PATH")


class App:
    def __init__(self):
        self.io = TranslationLayer(CONTROLLER, 9600)

        self.controllers = ControllerManager(io=self.io)

        self.db = Database()

        self.game = Game(control_manager=self.controllers)

        self.api_server = ApiServer(self)

    def start_api(self):
        # Flask must run in a thread to avoid blocking
        t = threading.Thread(
            target=lambda: self.api_server.run(
                host="0.0.0.0", port=5000, debug=False, use_reloader=False),
            daemon=True,
        )
        t.start()
        print("API server running on http://localhost:5000")

    def controller_update(self):
        result = self.io.update()
        if result:
            cid, controls, _ = result
            self.controllers.update_from_packet(cid, controls)

    def run(self):
        self.start_api()
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
