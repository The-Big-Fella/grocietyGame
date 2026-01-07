from flask import Flask, jsonify

from game.questions.questionlist import QuestionList


class ApiServer(Flask):
    def __init__(self, app):
        super().__init__(__name__)

        self.app = app

        self.add_url_rule("/getcontroller", "get_state",
                          self.getControllerState)

        self.add_url_rule("/getcurrentround", "get_round_state",
                          self.getRoundState)

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

        event = round.getEvent()

        questions = []
        roundstate = {}
        if isinstance(event, QuestionList):
            for q in event:
                question = {
                    "question": q.question,
                    "mood": q.mood,
                    "budget": q.budget,
                    "time": q.time,
                }
                questions.append(question)

            roundstate = {
                "id": round.id,
                "questions": questions,
            }

        return jsonify(roundstate)
