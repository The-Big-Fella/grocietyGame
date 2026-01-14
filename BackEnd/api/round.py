from flask import Blueprint, current_app, jsonify

class RoundAPI:
    def __init__(self, game_app):
        self.game_app = game_app
        self.bp = Blueprint("round_api", __name__)
        self.bp.add_url_rule("/api/getcurrentround", "get_round_state", self.get_round_state)

    def get_round_state(self):
        game = self.game_app.game
        current_round = game.current_round

        if not current_round:
            return jsonify({"error": "No active round"})

        # Only send question text
        event = current_round.getEvent()
        if event:
            questions = [{"question": q.question} for q in event]
        else:
            questions = []

        return jsonify({
            "id": current_round.id,
            "round_type": current_round.round_type,
            "questions": questions,
            "round_budget": game.budget_handler.max_round_budget,  # Round-specific budget
            "game_mood": game.mood  # Overall mood
        })
