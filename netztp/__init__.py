from flask import Flask
from netztp.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from netztp.eos import bp as eos
    app.register_blueprint(eos, url_prefix='/eos')

    from netztp.opengear import bp as opengear
    app.register_blueprint(opengear, url_prefix='/opengear')

    return app
