from flask import Blueprint, jsonify


class GameAPI:
    def __init__(self, app):
        self.app = app
        self.bp = Blueprint("game_api", __name__)

        self.bp.add_url_rule(
            "/getgamestate",
            "get_game_state",
            self.get_game_state
        )

    def get_game_state(self):
        game = self.app.game

        return jsonify({
            "state": game.state,
            "mood": game.mood,
            "budget": game.budget,
        })
