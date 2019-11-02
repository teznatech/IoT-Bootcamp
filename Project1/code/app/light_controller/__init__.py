from flask import Blueprint

bp = Blueprint('light', __name__)

from app.light_controller import routes