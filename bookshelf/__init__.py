import os
from flask import Flask

from bookshelf.config import CONFIGS

from bookshelf.extensions import db, migrate

def create_app(env: str | None = None) -> Flask:
    app = Flask(__name__)
    env = env or os.getenv("APP_ENV", "development")
    app.config.from_object(CONFIGS[env])

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models 
    from .api import register_blueprints
    from .errors import register_error_handlers

    register_blueprints(app)
    register_error_handlers(app)
    return app