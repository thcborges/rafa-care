from flask import Flask

from rafa_care.ext import config


def create_app():
    app = Flask(__name__)
    config.init_app(app)

    @app.get("/")
    def home():
        return "Hello, Rafa!"

    return app
