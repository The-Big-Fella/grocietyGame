from flask import Blueprint, jsonify


class ControllerAPI:
    def __init__(self, game_app):
        self.game_app = game_app
        self.bp = Blueprint("controller_api", __name__)
        self.bp.add_url_rule("/getcontroller", "get_controller_state", self.get_controller_state)

    def get_controller_state(self):
        controllers = self.game_app.game.controls.all_controllers()
        data = {}
        for c in controllers:
            data[c.get_controller_id()] = {
                "sliders": c.get_slider_data(),
                "button_state": c.get_button_state()
            }
        return jsonify(data)
