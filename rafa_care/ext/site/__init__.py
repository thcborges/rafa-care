from flask import Flask

from rafa_care.ext.site.controller import bp


def init_app(app: Flask):
    app.register_blueprint(bp)
