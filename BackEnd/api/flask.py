from flask import Flask, send_from_directory
from api import ControllerAPI, RoundAPI, GameAPI


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

    def index(self):
        return send_from_directory(
            self.app.static_folder,
            "index.html"
        )

    def run(self, **kwargs):
        self.app.run(**kwargs)
