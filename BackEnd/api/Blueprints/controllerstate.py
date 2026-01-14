from flask import Blueprint, jsonify


class ControllerBluePrint(Blueprint):
    def __init__(self, app):
        super().__init__("controllers", __name__)
        self.app = app.get_controllers()

        self.add_url_rule("/controllers_state",
                          "controllers_state", self.get_controllers_state)

    def get_controllers_state(self):
        return jsonify(self.app.get_controllers())
