from flask import Blueprint, current_app

import git

bp = Blueprint('pxe', __name__, static_folder='static',
                                template_folder='templates')

from netztp.pxe import routes

