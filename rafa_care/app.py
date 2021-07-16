from flask import Flask, render_template

from rafa_care.ext import config


def create_app():
    app = Flask(__name__)
    config.init_app(app)

    return app
