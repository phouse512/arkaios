from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template, request, jsonify, make_response, Response
from arkaios.models import Base, User, LargeGroup, SmallGroup, SmallGroupEvent, Attendee, LargeGroupAttendance, SmallGroupEventAttendance
from arkaios import config
from arkaios import helpers

import csv

from sqlalchemy import desc
from sqlalchemy.orm import load_only

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
db.Model = Base

@app.route('/admin/large-group/')
def large_group_overview():
	userCount = db.session.query(Attendee).count()
	return render_template('largegroup/overview.html')

@app.route('/admin/large-group/_get_overview_table')
def large_group_overview_table_admin():
	userCount = db.session.query(Attendee).count();

	selectedQuarter = "w14"
	attendanceArray = [[0 for i in range(10)] for j in range(userCount)]
	weeks = [range(11)]
	users = db.session.query(Attendee).options(load_only("id", "first_name", "last_name", "year"))
	weeked = db.session.query(LargeGroup).filter_by(quarter="w14").options(load_only("id"))

	userCount = 0
	weekCount = 0
	print weeks[0]
	for user in users:
		for week in weeks:
			try:
				val = db.session.query(LargeGroupAttendance).filter_by(large_group_id=week.id).filter_by(attendee_id=user.id).first()
				print val
				print "week: " + str(week.id) + " user: " + str(user.id)
				#print "value first time: " + str(val.first_time) + " value.count(): " + str(val.count())
				#first time case
				if(val.first_time == 1):
					attendanceArray[userCount][weekCount] = 2
				#normal attendee case
				elif(val is not None):
					attendanceArray[userCount][weekCount] = 1
				# no attendance case
				else:
					attendanceArray[userCount][weekCount] = 0
			except AttributeError,e:
				# if doesn't exist, assume no attendance
				print str(e)
				attendanceArray[userCount][weekCount] = 0
			weekCount += 1
		userCount += 1
		weekCount = 0
	return render_template('largegroup/_overview_table.html', attendance=attendanceArray, userInfo=users)

# Large group manage - collect record counts
@app.route('/admin/large-group/manage')
def large_group_manage():
	winter2014 = [0]*10
	spring2014 = [0]*10
	fall2014 = [0]*10

	for i in range(10):
		winter2014[i] = db.session.query(LargeGroup).filter_by(weekNumber=i+1).filter_by(quarter='w14').join(LargeGroup.large_group_attendance).count()
		spring2014[i] = db.session.query(LargeGroup).filter_by(weekNumber=i+1).filter_by(quarter='s14').join(LargeGroup.large_group_attendance).count()
		fall2014[i] = db.session.query(LargeGroup).filter_by(weekNumber=i+1).filter_by(quarter='f14').join(LargeGroup.large_group_attendance).count()

	return render_template('largegroup/manage.html', w14=winter2014, s14=spring2014, f14=fall2014)

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
	sort = request.args.get('sort', 0, type=int)
	sift = request.args.get('sift', 0, type=int)
	returnType = request.args.get('returnType', 0, type=int)

	sortingDictionary = {0: LargeGroupAttendance.id, 1: Attendee.year, 2: Attendee.first_name, 3: Attendee.last_name }

	# the ALL case of the page view - not implemented yet
	if week == -1:
		return render_template('largegroup/_full_attendance_table.html')

	# if event doesn't exist - catch the error and don't crash!!
	try:
		event_id = db.session.query(LargeGroup).filter_by(weekNumber=week).filter_by(quarter=quarter).first().id
	except AttributeError:
		# no event was found - display nothing yo
		return render_template('largegroup/_no_event_found.html')
	
	#sifting 
	if(sift == 0):
		attendance_records = db.session.query(LargeGroupAttendance).filter_by(large_group_id=event_id).join(LargeGroupAttendance.attendee).order_by(sortingDictionary[sort])
	elif(sift == 1):
		attendance_records = db.session.query(LargeGroupAttendance).filter_by(large_group_id=event_id).join(LargeGroupAttendance.attendee).filter_by(year="freshman").order_by(sortingDictionary[sort])
	elif(sift == 2):
		attendance_records = db.session.query(LargeGroupAttendance).filter_by(large_group_id=event_id).join(LargeGroupAttendance.attendee).filter_by(year="sophomore").order_by(sortingDictionary[sort])
	elif(sift == 3):
		attendance_records = db.session.query(LargeGroupAttendance).filter_by(large_group_id=event_id).join(LargeGroupAttendance.attendee).filter_by(year="junior").order_by(sortingDictionary[sort])	
	elif(sift == 4):
		attendance_records = db.session.query(LargeGroupAttendance).filter_by(large_group_id=event_id).join(LargeGroupAttendance.attendee).filter_by(year="senior").order_by(sortingDictionary[sort])	
	elif(sift == 5):
		attendance_records = db.session.query(LargeGroupAttendance).filter_by(large_group_id=event_id).join(LargeGroupAttendance.attendee).filter_by(year="other").order_by(sortingDictionary[sort])	
	elif(sift == 6):
		attendance_records = db.session.query(LargeGroupAttendance).filter_by(large_group_id=event_id).filter_by(first_time=1).join(LargeGroupAttendance.attendee).order_by(sortingDictionary[sort])
	
	if returnType == 0:
		return render_template('largegroup/_attendance_table.html', attendance=attendance_records)
	else:
		# first create
		fullArray = [1]
		columnDescription = ["Last Name", "First Name", "Email", "Dorm", "Year"]
		fullArray[0] = columnDescription

		for record in attendance_records:
			temp = [record.attendee.last_name, record.attendee.first_name, record.attendee.email, record.attendee.dorm, record.attendee.year]
			fullArray.append(temp)

		def generate():
			for row in fullArray:
				yield ','.join(row) + '\n'

		return Response(generate(), mimetype='text/csv', headers={"Content-Disposition":"attachment;filename=" + helpers.parseFileName(quarter, week)})

# Attendance Tracking
@app.route('/focus/<event_data>')
def large_group(event_data):
	quarter = event_data.split("-")[0]
	week = event_data.split("-")[1][1:]

	try:
		event_id = db.session.query(LargeGroup).filter_by(weekNumber=week).filter_by(quarter=quarter).first().id
	except AttributeError:
		# no event was found - display nothing yo
		new_event = LargeGroup(quarter=quarter, weekNumber=week, name="Focus")
		db.session.add(new_event)
		db.session.commit()

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