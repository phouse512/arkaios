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
def large_group_overview():
	user = db.session.query(User).filter_by(id=1)
	return render_template('largegroup/overview.html', user=user)

# Large Group Attendance Page
@app.route('/admin/large-group/<event_data>')
def large_group_attendance_admin(event_data):
	quarter = event_data
	#quarter = event_data.split("-")[0]
	#week = event_data.split("-")[1][1:]

	return render_template('largegroup/attendance.html', event_data=quarter)

# Large Group Attendance Data AJAX call
@app.route('/admin/large-group/_get_event_table')
def large_group_attendance_table_admin():
	quarter = request.args.get('quarter', "w14", type=str)
	week = request.args.get('week', 1, type=int)

	# if event doesn't exist - catch the error and don't crash!!
	try:
		event_id = db.session.query(LargeGroup).filter_by(weekNumber=week).filter_by(quarter=quarter).first().id

		attendance_records = db.session.query(LargeGroupAttendance).filter_by(large_group_id=event_id)
		return render_template('largegroup/_attendance_table.html', attendance=attendance_records)
	
	except AttributeError:
		# no event was found - display nothing yo
		return render_template('largegroup/_no_event_found.html')


# Attendance Tracking
@app.route('/focus/<event_data>')
def large_group(event_data):
	quarter = event_data.split("-")[0]
	week = event_data.split("-")[1][1:]
	return render_template('tracking/largegroup.html', quarter=quarter, week=week)

@app.route('/focus/_track')
def large_group_attendance_tracking():
	# gather event data
	quarter = request.args.get('quarter', "w14", type=str)
	week = request.args.get('week', 1, type=int)

	# gather user input
	inputFirstName = request.args.get('firstName')
	inputLastName = request.args.get('lastName')
	inputEmail = request.args.get('email')
	inputDorm = request.args.get('dorm')
	inputYear = request.args.get('year')
	errorArray = []

	# error handling
	if((not inputFirstName) or (not inputLastName) or (not inputEmail) or (not inputYear)):
		if(not inputFirstName):
			errorArray.append("firstName")
		if(not inputLastName):
			errorArray.append("lastName")
		if(not inputEmail):
			errorArray.append("email")
		if(not inputYear):
			errorArray.append("year")
		status = "error"
	else:
		# no errors - find out if this is a first time attendee
		event_id = db.session.query(LargeGroup).filter_by(weekNumber=week).filter_by(quarter=quarter).first().id
		user_lookup = db.session.query(Attendee).filter_by(email=inputEmail).count()

		if user_lookup:
			# if user exists
			user = db.session.query(Attendee).filter_by(email=inputEmail).first()
			user_attendance_lookup = db.session.query(LargeGroupAttendance).filter_by(large_group_id=event_id).filter_by(attendee_id=user.id).count()
			if user_attendance_lookup:
				# attendance record exists - almost nothing 
				status = "success"
			else:
				# attendance record doesn't exist - add it
				new_attendance = LargeGroupAttendance(large_group_id=event_id, attendee_id=user.id, first_time=0)
				db.session.add(new_attendance)
				db.session.commit()
				status = "success"
		else:	
			# if user dne
			new_user = Attendee(first_name=inputFirstName, last_name=inputLastName, year=inputYear, email=inputEmail, dorm=inputDorm)
			db.session.add(new_user)
			db.session.commit()
			new_attendance = LargeGroupAttendance(large_group_id=event_id, attendee_id=new_user.id, first_time=1)
			db.session.add(new_attendance)
			db.session.commit()
			status = "success"

	return jsonify(status=status, error=errorArray)

# Example of ajax route that returns JSON
@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)