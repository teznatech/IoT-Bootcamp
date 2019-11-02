from flask import Blueprint

bp = Blueprint('cam', __name__)

from app.camera import routes