from flask import Flask, render_template
import os


def create_app():
    app = Flask(__name__)
    netztp_env = os.getenv('NETZTP_ENV', 'DEFAULT').capitalize()
    app.config.from_object(f'netztp.config.{netztp_env}')

    with app.app_context():

        from netztp.eos import bp as eos
        app.register_blueprint(eos, url_prefix='/eos')

        from netztp.opengear import bp as opengear
        app.register_blueprint(opengear, url_prefix='/opengear')

        from netztp.pxe import bp as pxe
        app.register_blueprint(pxe, url_prefix='/pxe')

        @app.route('/')
        def index():
            urls = [url for url in app.url_map.iter_rules()]
            return render_template('index.html', urls=urls)

    return app
