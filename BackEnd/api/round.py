from flask import Blueprint, jsonify
from game.questions.questionlist import QuestionList


class RoundAPI:
    def __init__(self, app):
        self.app = app
        self.bp = Blueprint("round_api", __name__)

        self.bp.add_url_rule(
            "/getcurrentround",
            "get_round_state",
            self.get_round_state
        )

    def get_round_state(self):
        round = self.app.game.current_round

        if not round:
            return jsonify({})

        event = round.getEvent()

        if not isinstance(event, QuestionList):
            return jsonify({})

        questions = [
            {
                "question": q.question,
                "mood": q.mood,
                "budget": q.budget,
                "time": q.time,
            }
            for q in event
        ]

        return jsonify({
            "id": round.id,
            "questions": questions,
        })
