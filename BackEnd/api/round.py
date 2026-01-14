from flask import Blueprint, jsonify, request
import sqlite3
from game.questions.questionlist import QuestionList


class RoundAPI:
    def __init__(self, app):
        self.app = app
        self.bp = Blueprint("round_api", __name__, url_prefix="/api")

        # Events Routes
        self.bp.add_url_rule("/events", "list_events",
                             self.list_events, methods=["GET"])
        self.bp.add_url_rule("/events", "create_event",
                             self.create_event, methods=["POST"])
        self.bp.add_url_rule("/events/<int:event_id>",
                             "delete_event", self.delete_event, methods=["DELETE"])
        self.bp.add_url_rule("/events/<int:event_id>",
                             "update_event", self.update_event, methods=["PUT"])

        # Rounds Routes
        self.bp.add_url_rule("/rounds", "list_rounds",
                             self.list_rounds, methods=["GET"])
        self.bp.add_url_rule("/rounds", "create_round",
                             self.create_round, methods=["POST"])
        self.bp.add_url_rule("/rounds/<int:round_id>",
                             "delete_round", self.delete_round, methods=["DELETE"])

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

    def list_events(self):
        return jsonify(self.app.db.get_events())

    def create_event(self):
        data = request.json
        self.app.db.add_event(data["name"])
        return jsonify({"status": "success"}), 201

    def update_event(self, event_id):
        data = request.json
        self.app.db.update_event(event_id, data["name"])
        return jsonify({"status": "updated"})

    def delete_event(self, event_id):
        try:
            self.app.db.delete_event(event_id)
            return jsonify({"status": "success"})
        except sqlite3.IntegrityError:
            return jsonify({"error": "Cannot delete event while it has rounds"}), 400

    def list_rounds(self):
        return jsonify(self.app.db.get_rounds())

    def create_round(self):
        data = request.json
        try:
            round_id = self.app.db.add_round(
                data["event_id"], data["round_number"])
            return jsonify({"id": round_id}), 201
        except sqlite3.IntegrityError:
            return jsonify({"error": "This round number already exists for this event"}), 400

    def delete_round(self, round_id):
        try:
            self.app.db.delete_round(round_id)
            return jsonify({"status": "success"})
        except sqlite3.IntegrityError:
            return jsonify({"error": "Cannot delete round while it has questions"}), 400

    def register(self):
        self.app.register_blueprint(self.bp)
