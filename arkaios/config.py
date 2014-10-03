import os
PWD = os.path.abspath(os.curdir)

DEBUG=True
#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
#SQLALCHEMY_DATABASE_URI = 'postgres://PhilipHouse:house@localhost/arkaios'
SQLALCHEMY_DATABASE_URI = 'postgres://gtwnxaeulqztlh:Af5wrfurq510fqonyoFiZryaFg@ec2-54-197-241-91.compute-1.amazonaws.com:5432/d5uaju8veb38j0'
SECRET_KEY = 'thisissecret'
SESSION_PROTECTION = 'stroang'
