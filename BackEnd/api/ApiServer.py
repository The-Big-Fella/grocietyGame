from flask import Flask, send_from_directory
from api.Blueprints import GameBluePrint, ControllerBluePrint


class ApiServer:
    def __init__(self, app):
        self.flask = Flask(
            __name__,
            static_folder="Static",
            static_url_path=""
        )

        self.app = app

        self.register_blueprints()
        self.flask.add_url_rule("/", "frontend", self.frontend)
        self.flask.add_url_rule("/monitor", "monitor", self.monitor)

    def register_blueprints(self):
        self.flask.register_blueprint(
            GameBluePrint(self.app)
        )
        self.flask.register_blueprint(
            ControllerBluePrint(self.app)
        )

    def frontend(self):
        return send_from_directory(
            self.flask.static_folder,
            "frontend/index.html"
        )

    def monitor(self):
        return send_from_directory(
            self.flask.static_folder,
            "monitor/index.html"
        )

    def run(self, **kwargs):
        self.flask.run(**kwargs)
