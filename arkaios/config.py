import os
PWD = os.path.abspath(os.curdir)

DEBUG=True
#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_DATABASE_URI = 'postgres://PhilipHouse:house@localhost/arkaios'
SECRET_KEY = 'thisissecret'
SESSION_PROTECTION = 'stroang'
