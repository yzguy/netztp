from flask import Blueprint

bp = Blueprint('eos', __name__, static_folder='static')

from app.eos import routes
