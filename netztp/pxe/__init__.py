from flask import Blueprint, current_app

from netztp.pxe.datastore import Datastore

bp = Blueprint('pxe', __name__, static_folder='static',
                                template_folder='templates')

datastore = Datastore(current_app.config['DATASTORE_SERVER'])

from netztp.pxe import routes

