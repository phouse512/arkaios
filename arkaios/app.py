from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template

from arkaios.models import Base, User
from arkaios import config

app = Flask(__name__)
app.config.from_object(config)



db = SQLAlchemy(app)
db.Model = Base

@app.route('/admin/large-group')
def largeGroupOverview():
	user = db.session.query(User)
	return render_template('largegroup/overview.html', user=user)

@app.route('/admin/large-group/<int:event_id>')
def largeGroupAttendance(event_id):
	return render_template('largegroup/attendance.html')

@app.route('/focus')
def largegroup():
	return 'Focus work'