from flask import Blueprint

bp = Blueprint('eos', __name__, static_folder='static')

from netztp.eos import routes
