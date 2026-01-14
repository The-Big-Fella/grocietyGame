from flask import Flask, jsonify, send_from_directory

from game.questions.questionlist import QuestionList


class ApiServer(Flask):
    def __init__(self, app):
        super().__init__(__name__, static_folder="./static/")

        self.app = app

        self.add_url_rule("/getcontroller", "get_state",
                          self.getControllerState)

        self.add_url_rule("/getcurrentround", "get_round_state",
                          self.getRoundState)

        self.add_url_rule("/", "index", self.index)

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
