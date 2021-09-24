from flask import Flask, render_template

import os, git, shutil

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

        git_url = 'https://{}@{}'.format(
                    app.config['GITHUB_TOKEN'],
                    app.config['PXE_CONFIG_REPO']
                )

        if os.path.isdir(pxe.static_folder):
            repo = git.Repo(pxe.static_folder)
            repo.remotes.origin.pull('master')
        else:
            git.Repo.clone_from(git_url, pxe.static_folder)

        @app.route('/')
        def index():
            urls = [url for url in app.url_map.iter_rules()]
            return render_template('index.html', urls=urls)

    return app
