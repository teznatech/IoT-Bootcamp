from flask import Blueprint

bp = Blueprint('routine', __name__)

from app.routine_control import routes