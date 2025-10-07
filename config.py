import os
import configparser
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, '.env'))

config = configparser.ConfigParser()
config.read(os.path.join(basedir, 'config.ini'))

class Config(object):
    RATE_LIMIT = config["DEFAULT"]["RATE_LIMIT"]
    RATE_WINDOW = config["DEFAULT"]["RATE_WINDOW"]
    ENABLE_RATE_LIMITING = config["DEFAULT"]["ENABLE_RATE_LIMITING"]
    SECRET_KEY = os.getenv("SECRET_KEY")
    DB_URL_FROM_ENV = os.getenv("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = DB_URL_FROM_ENV or 'sqlite:///' + os.path.join(basedir, 'devdatabase.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
