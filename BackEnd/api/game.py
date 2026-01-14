from flask import Blueprint, jsonify

class GameAPI:
    def __init__(self, app):
        self.app = app
        self.bp = Blueprint("game_api", __name__)

        # Existing endpoint
        self.bp.add_url_rule(
            "/getgamestate",
            "get_game_state",
            self.get_game_state
        )

    def get_game_state(self):
        game = self.app.game
        decay = game.mood_decay

        import time
        elapsed = int(time.monotonic() - decay.start_time) if decay.start_time else 0

        # Build penalties with reached status
        penalties = [
            {"time": t, "amount": a, "reached": i < decay.next_index}
            for i, (t, a) in enumerate(decay.timeline)
        ]

        post_penalty = {
            "delay": decay.post_penalty_delay,
            "amount": decay.post_penalty_amount,
            "started": decay.post_penalty_started
        }

        # Add controller slider states
        controllers_data = {}
        for c in game.controls.all_controllers():
            controllers_data[c.get_controller_id()] = {
                "sliders": c.get_slider_data(),
                "button_state": c.get_button_state()
            }

        return jsonify({
            "state": game.state,
            "mood": game.mood,
            "budget": game.budget,
            "elapsed": elapsed,
            "penalties": penalties,
            "post_penalty": post_penalty,
            "controllers": controllers_data  # <-- new
        })
