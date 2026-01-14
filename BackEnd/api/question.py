from flask import Blueprint, request, jsonify
import sqlite3


class QuestionAPI:
    def __init__(self, app):
        self.app = app
        self.bp = Blueprint("question_api", __name__, url_prefix="/api")

        # GET all questions
        self.bp.add_url_rule("/questions", "list_questions",
                             self.list_questions, methods=["GET"])

        # POST new question
        self.bp.add_url_rule("/questions", "create_question",
                             self.create_question, methods=["POST"])

        # DELETE a specific question
        self.bp.add_url_rule("/questions/<int:question_id>",
                             "delete_question", self.delete_question, methods=["DELETE"])

        # PUT (Update) a specific question
        self.bp.add_url_rule("/questions/<int:question_id>",
                             "update_question", self.update_question, methods=["PUT"])

    def create_question(self):
        data = request.get_json()
        required = ["round_id", "type_id", "text", "budget", "mood"]
        if not all(k in data for k in required):
            return jsonify({"error": "Missing fields"}), 400

        try:
            self.app.db.add_question(
                round_id=data["round_id"],
                type_id=data["type_id"],
                text=data["text"],
                budget=data["budget"],
                mood=data["mood"]
            )
            return jsonify({"status": "success"}), 201
        except sqlite3.IntegrityError as e:
            return jsonify({"error": f"Database integrity error: {str(e)}"}), 400
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal error"}), 500

    def list_questions(self):
        try:
            questions = self.app.db.get_questions()
            print(questions)
            return jsonify(questions), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def delete_question(self, question_id):
        """Removes a question by its ID"""
        try:
            self.app.db.delete_question(question_id)
            return jsonify({"status": "deleted"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def update_question(self, question_id):
        """Updates question details"""
        data = request.get_json()
        try:
            self.app.db.update_question(
                question_id=question_id,
                text=data.get("text"),
                budget=data.get("budget"),
                mood=data.get("mood")
            )
            return jsonify({"status": "updated"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def register(self):
        self.app.register_blueprint(self.bp)
