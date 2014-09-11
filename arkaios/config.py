import os
PWD = os.path.abspath(os.curdir)

DEBUG=True
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SECRET_KEY = 'thisissecret'
SESSION_PROTECTION = 'strong'
