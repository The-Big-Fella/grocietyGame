from flask import Blueprint, jsonify


class ControllerAPI:
    def __init__(self, app):
        self.app = app
        self.bp = Blueprint("controller_api", __name__)

        self.bp.add_url_rule(
            "/getcontroller",
            "get_controller_state",
            self.get_controller_state
        )

    def get_controller_state(self):
        controllers = self.app.controllers.get_controllers()

        state = {
            c.get_controller_id(): {
                "sliders": c.get_slider_data(),
                "button_state": c.get_button_state(),
            }
            for c in controllers.values()
        }

        return jsonify(state)
