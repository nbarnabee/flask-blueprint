import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from api.config import config

# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()


# App factory function
def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "development")

    # instantiate Flask app
    app = Flask(__name__)

    # apply config defined in api.config.py
    app.config.from_object(config[config_name])

    # instantiate extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints below
    from api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # basic shell context processor, spares us having to type
    # `from app import db` each time we want to experiment using
    # the flask shell. Could be expanded to also pre-import our
    # models, etc.
    @app.shell_context_processor
    def make_shell_context():
        return {"app": app, "db": db}

    return app
