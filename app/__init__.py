from flask import Flask
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.eos import bp as eos
    app.register_blueprint(eos, url_prefix='/eos')

    return app
