import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Default(object):
    DEBUG = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///{}'.format(os.path.join(basedir, 'netztp.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JSONIFY_PRETTYPRINT_REGULAR = True

    LOG_DESTINATIONS = [{
        'destination': '192.168.50.2:514',
        'level': 'DEBUG'
    }]

    FIRMWARE_SERVER = 'https://firmware.yzguy.io'
    EOS_VERSIONS = {
        '4.21.7.1M': 'vEOS-lab-4.21.7.1M.swi',
        '4.22.2.1F': 'vEOS-lab-4.22.2.1F.swi',
        '4.23.0.1F': 'vEOS-lab-4.23.0.1F.swi',
        '4.24.2.1F': 'vEOS-lab-4.24.2.1F.swi',
        'default': '4.24.2.1F'
    }

class Development(Default):
    FLASK_ENV = 'development'
    DEBUG = True

class Production(Default):
    FLASK_ENV = 'production'
