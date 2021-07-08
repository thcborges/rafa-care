from flask import Flask
from flask_migrate import Migrate

from rafa_care.ext.db import db
from rafa_care.ext.models import *  # noqa

migrate = Migrate()


def init_app(app: Flask):
    migrate.init_app(app, db)
