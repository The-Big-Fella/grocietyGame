import time
import os
import signal
import sys

from controls import ControllerManager, TranslationLayer
from game import Game
from api import ApiServer

PORT = 5000
HOST = "0.0.0.0"
CONTROLLER = os.getenv("CONTROLLER_PATH")


class App:
    def __init__(self):
        self.running = True

        # controls
        self.io = TranslationLayer(CONTROLLER, 9600)
        self.controllers = ControllerManager(io=self.io)

        # backend
        self.game = Game(self.controllers, self)
        self.api = ApiServer(self)

        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

    def get_game(self) -> Game:
        return self.game

    def shutdown(self, signum, frame):
        print(f"\nShutting down gracefully (signal {signum})...")
        self.running = False

    def controller_update(self):
        result = self.io.update()
        if result:
            cid, controls, _ = result
            self.controllers.update_from_packet(cid, controls)

    def run(self):
        # self.game.start_game()

        try:
            while self.running:
                self.controller_update()
                self.game.update()
                time.sleep(0.001)
        finally:
            self.cleanup()

    def cleanup(self):
        try:
            if hasattr(self.io, "close"):
                self.io.close()
        except Exception as e:
            print("Error during cleanup:", e)

        print("Shutdown complete.")
        sys.exit(0)


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
