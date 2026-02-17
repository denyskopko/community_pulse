from flask import Flask
from flask_migrate import Migrate

from core.config import settings
from routers.questions import questions_bp
from core.db import db
from models import *


def init_database(app: Flask):
    db.init_app(app)

    migrate = Migrate()
    migrate.init_app(app, db)


def register_routers(app: Flask):
    app.register_blueprint(questions_bp)


def create_app(app: Flask):
    app.config.update(settings.get_flask_config())

    init_database(app)

    register_routers(app)
