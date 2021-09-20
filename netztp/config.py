import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Default(object):
    DEBUG = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///{}'.format(os.path.join(basedir, 'netztp.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    INVENTORY_API_TOKEN = os.environ.get('INVENTORY_API_TOKEN')

    LOG_DESTINATIONS = [{
        'destination': '192.168.50.2:514',
        'level': 'DEBUG'
    }]

    FIRMWARE_SERVER = 'http://firmware.yzguy.io'

    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

    PXE_CONFIG_REPO = 'github.com/yzguy/netztp-configs.git'


class Development(Default):
    FLASK_ENV = 'development'
    DEBUG = True

class Production(Default):
    FLASK_ENV = 'production'
