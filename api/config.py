import os
from pathlib import Path


class BaseConfig:
    """Base config"""

    # application root dir, where app.py lives
    BASE_DIR = Path(__file__).parent.parent

    TESTING = False

    # requires extra memory and should be disabled if not needed
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # sqlite for now; just change the URI to use with another db
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite3"
    )


class DevelopmentConfig(BaseConfig):
    """Development config"""

    DEBUG = True


class ProductionConfig(BaseConfig):
    """Production config"""

    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
