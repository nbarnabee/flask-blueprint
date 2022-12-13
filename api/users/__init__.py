from flask import Blueprint

# example use of the blueprint pattern
users_blueprint = Blueprint(
    "users", __name__, url_prefix="/users", template_folder="templates"
)

# if we later add user-related tasks in a api.users.tasks.py file, we'll have to import them here as well.
from . import models  # noqa
