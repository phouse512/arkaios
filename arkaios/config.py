import os
PWD = os.path.abspath(os.curdir)

DEBUG=True
SQLALCHEMY_DATABASE_URI = 'sqlite:///arkaios.db'
SECRET_KEY = 'thisissecret'
SESSION_PROTECTION = 'strong'