from flask import Flask
from netztp.inventory import Inventory

import os

inventory = Inventory()

def create_app():
    app = Flask(__name__)
    netztp_env = os.getenv('NETZTP_ENV', 'DEFAULT').capitalize()
    app.config.from_object(f'netztp.config.{netztp_env}')

    inventory.authenticate(app.config['INVENTORY_API_TOKEN'])

    from netztp.eos import bp as eos
    app.register_blueprint(eos, url_prefix='/eos')

    from netztp.opengear import bp as opengear
    app.register_blueprint(opengear, url_prefix='/opengear')

    return app
