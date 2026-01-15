from flask import Blueprint, jsonify


class GameBluePrint(Blueprint):
    def __init__(self, app):
        super().__init__("Game", __name__)
        self.app = app.get_game()
        print(self.app)

        self.add_url_rule("/game_state", "game_state", self.get_game_state)
        self.add_url_rule("/current_round", "current_round",
                          self.get_game_round)

    def get_game_state(self):
        return jsonify(self.app.get_state())

    def get_game_round(self):
        return jsonify(self.app.get_current_round())
