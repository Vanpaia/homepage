import os
import configparser
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, '.env'))

config = configparser.ConfigParser()
config.read(os.path.join(basedir, 'config.ini'))


host = config["DEFAULT"]["host"]
port = config["DEFAULT"]["port"]
dbname = config["DEFAULT"]["dbname"]
user = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")
RATE_LIMIT = os.getenv("RATE_LIMIT")
RATE_WINDOW = os.getenv("RATE_WINDOW")
ENABLE_RATE_LIMITING = os.getenv("ENABLE_RATE_LIMITING")

class Config(object):
#    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}' or 'sqlite:///' + os.path.join(basedir, 'devdatabase.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'devdatabase.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
