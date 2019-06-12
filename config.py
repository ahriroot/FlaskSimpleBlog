import os

DEBUG = True

SECRET_KEY = os.urandom(24)

# HOSTNAME = ''
# PORT = ''
DATABASE = 'db.sqlite3'
# USERNAME = ''
# PASSWORD = ''
# DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
DB_URI = 'sqlite:///{}'.format(DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = '/media/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
