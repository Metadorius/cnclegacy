import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'lolkek'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+mysqldb://root:dev2703@localhost:3306/cnclegacy'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
