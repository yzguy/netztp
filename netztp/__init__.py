from flask import Flask, render_template
from netztp.inventory import Inventory

import os

inventory = Inventory()

def create_app():
    app = Flask(__name__)
    netztp_env = os.getenv('NETZTP_ENV', 'DEFAULT').capitalize()
    app.config.from_object(f'netztp.config.{netztp_env}')

    from netztp.eos import bp as eos
    app.register_blueprint(eos, url_prefix='/eos')

    from netztp.opengear import bp as opengear
    app.register_blueprint(opengear, url_prefix='/opengear')

    @app.route('/')
    def index():
        urls = [url for url in app.url_map.iter_rules()]
        return render_template('index.html', urls=urls)

    return app
