from flask import Flask

from rafa_care.ext.site.route import bp


def init_app(app: Flask):
    app.register_blueprint(bp)
