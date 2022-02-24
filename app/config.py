import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'thisisasecret'

VERSION = '0.1'  # Across config.py, app.py, ../setup.py

PG_USERNAME = os.getenv('PG_USERNAME')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_NAME = os.getenv('PG_NAME')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')

MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_NAME = os.getenv('MYSQL_NAME')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')

SQLALCHEMY_DATABASE_URI = f'postgresql://{PG_USERNAME}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_NAME}'

SQLALCHEMY_BINDS = {  # https://flask-sqlalchemy.palletsprojects.com/en/2.x/binds/
    'DB2': f'mysql+mysqldb://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_NAME}',
}

SQLALCHEMY_TRACK_MODIFICATIONS = False

JSONIFY_PRETTYPRINT_REGULAR = True

CORS_HEADERS = 'Content-Type'

SESSION_TYPE = 'filesystem'

SQLALCHEMY_POOL_TIMEOUT = 300

SQLALCHEMY_POOL_SIZE = 100

SQLALCHEMY_POOL_RECYCLE = 280
