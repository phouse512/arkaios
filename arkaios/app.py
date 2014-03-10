from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template, request, jsonify

from arkaios.models import Base, User, LargeGroup, SmallGroup, SmallGroupEvent, Attendee, LargeGroupAttendance, SmallGroupEventAttendance
from arkaios import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
db.Model = Base

@app.route('/admin/large-group/')
def largeGroupOverview():
	user = db.session.query(User).filter_by(id=1)
	return render_template('largegroup/overview.html', user=user)

@app.route('/admin/large-group/<event_data>')
def largeGroupAttendance(event_data):
	quarter = event_data.split("-")[0]
	week = event_data.split("-")[1][1:]

	return render_template('largegroup/attendance.html', event_data=quarter)


# Attendance Tracking
@app.route('/focus/<event_data>')
def large_group(event_data):
	quarter = event_data.split("-")[0]
	week = event_data.split("-")[1][1:]
	return render_template('tracking/largegroup.html', quarter=quarter, week=week)

@app.route('/focus/_track')
def large_group_attendance():
	# gather event data
	quarter = request.args.get('quarter', "w14", type=str)
	week = request.args.get('week', 1, type=int)

	# gather user input
	inputFirstName = request.args.get('firstName')
	inputLastName = request.args.get('lastName')
	inputEmail = request.args.get('email')
	inputDorm = request.args.get('dorm')
	inputYear = request.args.get('year')

	# error handling
	if((not inputFirstName) or (not inputLastName) or (not inputEmail) or (not inputYear)):
		errorArray = []
		if(not inputFirstName):
			errorArray.append("firstName")
		if(not inputLastName):
			errorArray.append("lastName")
		if(not inputEmail):
			errorArray.append("email")
		if(not inputYear):
			errorArray.append("year")

		return jsonify(error=errorArray)

	# find out if this is a first time attendee
	event_id = db.session.query(LargeGroup).filter_by(weekNumber=week).filter_by(quarter=quarter).first().id
	user_lookup = db.session.query(Attendee).filter_by(email=inputEmail).count()


	if user_lookup:
		# if user exists
		user = db.session.query(Attendee).filter_by(email=inputEmail).first()
		user_attendance_lookup = db.session.query(LargeGroupAttendance).filter_by(large_group_id=event_id).filter_by(attendee_id=user.id).count()
		if user_attendance_lookup:
			# attendance record exists - almost nothing 
			status = "attendance record already exists - nothing needs to be done"
		else:
			# attendance record doesn't exist - add it
			status = "attendance added now"
			new_attendance = LargeGroupAttendance(large_group_id=event_id, attendee_id=user.id, first_time=0)
			db.session.add(new_attendance)
			db.session.commit()
	else:	
		# if user dne
		status = "we did not find the attendeee.....we shall proceed and build something new"
		new_user = Attendee(first_name=inputFirstName, last_name=inputLastName, year=inputYear, email=inputEmail, dorm=inputDorm)
		db.session.add(new_user)
		db.session.commit()
		new_attendance = LargeGroupAttendance(large_group_id=event_id, attendee_id=new_user.id, first_time=1)
		db.session.add(new_attendance)
		db.session.commit()
	return jsonify(status=status)


# Example of ajax route that returns JSON
@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)