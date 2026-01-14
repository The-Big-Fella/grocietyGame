from flask import Flask
from api.Blueprints import GameBluePrint


class ApiServer:
    def __init__(self, app):
        self.flask = Flask(
            __name__,
            static_folder="static",
            static_url_path=""
        )

        self.app = app

    def register_blueprints(self):
        self.flask.register_blueprint(
            GameBluePrint(self.app)
        )

    def run(self, **kwargs):
        self.flask.run(**kwargs)
