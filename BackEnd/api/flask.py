from flask import Flask, send_from_directory
from api import ControllerAPI, RoundAPI, GameAPI, QuestionAPI


class ApiServer:
    def __init__(self, app):
        self.app = Flask(
            __name__,
            static_folder="static",
            static_url_path=""
        )

        self.game_app = app

        self._register_blueprints()

        self.app.add_url_rule("/", "index", self.index)
        self.app.add_url_rule("/crud", "crud", self.crud)

    def _register_blueprints(self):
        self.app.register_blueprint(
            ControllerAPI(self.game_app).bp
        )
        self.app.register_blueprint(
            RoundAPI(self.game_app).bp
        )
        self.app.register_blueprint(
            GameAPI(self.game_app).bp
        )
        self.app.register_blueprint(
            QuestionAPI(self.game_app).bp
        )

    def index(self):
        return send_from_directory(self.static_folder, "index.html")

    def getControllerState(self):
        controllers = self.app.controllers.get_controllers()

        print(controllers)
        controllerState = {}
        for controller in controllers.values():
            controllerState[controller.get_controller_id()] = {
                "sliders": controller.get_slider_data(),
                "button_state": controller.get_button_state(),
            }

        return jsonify(controllerState)

    def getRoundState(self):
        round = self.app.game.current_round

        if not round:
            return jsonify()

        event = round.getEvent()
        questions = []
        roundstate = {}
        if isinstance(event, QuestionList):
            for q in event:
                question = {
                    "question": q.question,
                    "mood": q.mood,
                    "time": q.time,
                }
                questions.append(question)

            roundstate = {
                "id": round.id,
                "questions": questions,
            }

        return jsonify(roundstate)
