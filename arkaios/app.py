#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template, redirect, url_for, request, jsonify, make_response, Response, flash
from arkaios.models import Base, User, LargeGroup, SmallGroup, SmallGroupEvent, Attendee, LargeGroupAttendance, SmallGroupEventAttendance
from arkaios import config
from arkaios import helpers

import csv
import json

from sqlalchemy import desc, and_
from sqlalchemy.orm import load_only

app = Flask(__name__)
app.config.from_object(config)

app.debug = True

db = SQLAlchemy(app)
db.Model = Base

@app.route('/admin/large-group/')
def large_group_overview():
	userCount = db.session.query(Attendee).count()
	return render_template('largegroup/overview.html')

@app.route('/admin/large-group/_get_overview_graphs/<quarter>')
def large_group_overview_graphs_admin(quarter):
	weeks = [0 for i in range(10)]
	weeklyCount = []
	yearCount = []
	weekDB = db.session.query(LargeGroup).filter_by(quarter=quarter).options(load_only("id"))
	siftingDictionary = {1: "freshman", 2: "sophomore", 3: "junior", 4: "senior", 5: "other" }
	# set up full quarter week array with db ID's if exists, 0 otherwise
	for week in weekDB:
		try:
			weeks[int(week.weekNumber)-1] = week.id
		except ValueError,e:
			print str(e)

	for week in weeks:
		try:
			currentTotal = db.session.query(LargeGroupAttendance).filter_by(large_group_id=week).count()
			weeklyCount.append(currentTotal)
		except AttributeError,e:
			weeklyCount.append(0)

	slimWeeks = [x for x in weeks if x != 0]

	for year in siftingDictionary:
		try:
			currentTotal = db.session.query(LargeGroupAttendance).filter(LargeGroupAttendance.large_group_id.in_(slimWeeks)).join(LargeGroupAttendance.attendee).filter_by(year=siftingDictionary[year]).count()
			yearCount.append(currentTotal)
		except AttributeError,e:
			yearCount.append(0)

	
	return jsonify(week=weeklyCount, year=yearCount)

@app.route('/admin/large-group/_get_overview_table')
def large_group_overview_table_admin():
	sortingDictionary = {0: Attendee.id, 1: Attendee.year, 2: Attendee.first_name, 3: Attendee.last_name }
	siftingDictionary = {1: "freshman", 2: "sophomore", 3: "junior", 4: "senior", 5: "other" }

	# get params
	quarter = request.args.get('quarter', "w14", type=str)
	sort = request.args.get('sort', 0, type=int)
	sift = request.args.get('sift', 0, type=int)

	weeks = [0 for i in range(10)]
	if (sift == 0):
		users = db.session.query(Attendee).order_by(sortingDictionary[sort]).options(load_only("id", "first_name", "last_name", "year"))
		userCount = db.session.query(Attendee).order_by(sortingDictionary[sort]).options(load_only("id", "first_name", "last_name", "year")).count()
	else:
		users = db.session.query(Attendee).filter_by(year=siftingDictionary[sift]).order_by(sortingDictionary[sort]).options(load_only("id", "first_name", "last_name", "year"))
		userCount = db.session.query(Attendee).filter_by(year=siftingDictionary[sift]).order_by(sortingDictionary[sort]).options(load_only("id", "first_name", "last_name", "year")).count()

	attendanceArray = [[0 for i in range(10)] for j in range(userCount)]
	weekDB = db.session.query(LargeGroup).filter_by(quarter=quarter).options(load_only("id"))

	# set up full quarter week array with db ID's if exists, 0 otherwise
	for week in weekDB:
		try:
			weeks[int(week.weekNumber)-1] = week.id
		except ValueError,e:
			print str(e)
	#print weeks
	userCount, weekCount = 0, 0
	# iterate through full overview table
	for user in users:
		for week in weeks:
			try:
				val = db.session.query(LargeGroupAttendance).filter_by(large_group_id=week).filter_by(attendee_id=user.id).first()
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
	#print attendanceArray
	return render_template('largegroup/_overview_table.html', attendance=attendanceArray, userInfo=users)

# Large group manage - collect record counts
@app.route('/admin/large-group/manage')
def large_group_manage():
	fall2014 = [0]*10
	winter2015 = [0]*10
	spring2015 = [0]*10

	for i in range(10):
		fall2014[i] = db.session.query(LargeGroup).filter_by(weekNumber=i+1).filter_by(quarter='f14').join(LargeGroup.large_group_attendance).count()
		winter2015[i] = db.session.query(LargeGroup).filter_by(weekNumber=i+1).filter_by(quarter='w15').join(LargeGroup.large_group_attendance).count()
		spring2015[i] = db.session.query(LargeGroup).filter_by(weekNumber=i+1).filter_by(quarter='s15').join(LargeGroup.large_group_attendance).count()

	return render_template('largegroup/manage.html', f14=fall2014, w15=winter2015, s15=spring2015)

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
			new_user = Attendee(first_name=inputFirstName, last_name=inputLastName, 
					year=inputYear, email=inputEmail, dorm=inputDorm)
			db.session.add(new_user)
			db.session.commit()
			new_attendance = LargeGroupAttendance(large_group_id=event_id, attendee_id=new_user.id, first_time=1)
			db.session.add(new_attendance)
			db.session.commit()
			status = "success"

	return jsonify(status=status, error=errorArray)


# auto suggester for focus
@app.route('/focus/_search')
def large_group_attendance_search():
	inputFirstName = request.args.get('firstName')
	inputLastName = request.args.get('lastName')
	inputEmail = request.args.get('email')
	inputDorm = request.args.get('dorm')
	inputYear = request.args.get('year')

	sql = helpers.searchConstruction({'first_name': inputFirstName, 'last_name': inputLastName, 
			'email': inputEmail, 'dorm': inputDorm, 'year': inputYear})
	query = db.session.query(Attendee).filter(eval(sql)).limit(8);
	
	output = []
	for record in query:
		output.append(json.dumps({'id': record.id, 'firstname': record.first_name, 
				'lastname': record.last_name, 'year': record.year, 'dorm': record.dorm, 
				'email': record.email}))

	return jsonify(results=output)


##################################
#								 #
#  Family group leaders portion  #
#								 #
##################################

@app.route('/family-group/<fg_id>/overview')
def family_group_leader_overview(fg_id):

	return render_template('smallgroup/overview.html',id=fg_id)

@app.route('/family-group/<fg_id>/_overview_table')
def family_group_leader_overview_table(fg_id):

	# get params
	quarter = request.args.get('quarter', "f14", type=str)
	# for now quarter = 'f14'

	weeks = [0 for i in range(10)]

	users = db.session.query(SmallGroupEventAttendance).join(SmallGroupEventAttendance.small_group_event).join(SmallGroupEvent.small_group).filter_by(id=fg_id).distinct()


	norepeat = []
	finalList = []
	for val in users:	
		if val.attendee.id not in [x.attendee.id for x in norepeat]:
			finalList.append(val)
		norepeat.append(val)
	
	for y in finalList:
		print y

	attendanceArray = [[0 for i in range(10)] for j in range(len(finalList))]
	weekDB = db.session.query(SmallGroupEvent).filter_by(small_group_id=fg_id).filter_by(quarter=quarter).options(load_only("id"))

	# set up full quarter week array with db ID's if exists, 0 otherwise
	for week in weekDB:
		try:
			weeks[int(week.weekNumber)-1] = week.id
		except ValueError,e:
			print str(e)
	#print weeks
	userCount, weekCount = 0, 0
	# iterate through full overview table
	for user in finalList:
		for week in weeks:
			try:
				val = db.session.query(SmallGroupEventAttendance).filter_by(small_group_event_id=week).filter_by(attendee_id=user.attendee.id).first()

				if(val is not None):
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
	print attendanceArray
	print finalList
	return render_template('smallgroup/_overview_table.html', attendance=attendanceArray, userInfo=finalList)


# high level view of quarters/weeks before allowing for attendance modification
@app.route('/family-group/<fg_id>/manage')
def family_group_leader_manage(fg_id):
	fall2014 = [0]*10
	winter2015 = [0]*10
	spring2015 = [0]*10

	for i in range(10):
		fall2014[i] = db.session.query(SmallGroupEvent).filter_by(small_group_id=fg_id).filter_by(weekNumber=i+1).filter_by(quarter='f14').join(SmallGroupEvent.small_group_event_attendance).count()
		winter2015[i] = db.session.query(SmallGroupEvent).filter_by(small_group_id=fg_id).filter_by(weekNumber=i+1).filter_by(quarter='w15').join(SmallGroupEvent.small_group_event_attendance).count()
		spring2015[i] = db.session.query(SmallGroupEvent).filter_by(small_group_id=fg_id).filter_by(weekNumber=i+1).filter_by(quarter='s15').join(SmallGroupEvent.small_group_event_attendance).count()

	return render_template('smallgroup/manage.html', f14=fall2014, w15=winter2015, s15=spring2015)

@app.route('/family-group/<fg_id>/attendance/<event_id>')
def family_group_event_attendance(fg_id, event_id):
	attendance = db.session.query(SmallGroupEventAttendance).join(SmallGroupEventAttendance.small_group_event).join(SmallGroupEvent.small_group).filter_by(id=fg_id).distinct()

	norepeat = []
	existing = []
	finalList = []
	for val in attendance:	
		if val.attendee.id not in [x.attendee.id for x in norepeat]:
			exists = db.session.query(SmallGroupEventAttendance).filter_by(attendee_id=val.attendee.id).join(SmallGroupEventAttendance.small_group_event).filter_by(id=event_id).count()
			if(exists > 0):	
				existing.append(1)
			else:
				existing.append(0)
			finalList.append(val)
		norepeat.append(val)
	
	return render_template('smallgroup/edit.html', records=finalList, existing=existing, currentEventId=event_id, fgId=fg_id)

@app.route('/family-group/_get_users')
def family_group_all_users():
	attendees = db.session.query(Attendee).all()

	userList = []
	for i in attendees:
		temp = {
			'name': i.first_name + " " + i.last_name,
			'id': i.id
		}
		userList.append(temp)

	return jsonify(attendees=userList)

# save the family gorup event attendance
@app.route('/family-group/_save_attendance', methods=['POST'])
def family_group_save_attendance():	
	newAttending = set(json.loads(request.form['selectedPeople']))
	event = request.form['currentEvent']
	fg = request.form['currentFG']

	#get existing
	existingAttendees = db.session.query(SmallGroupEventAttendance).filter_by(small_group_event_id=event)

	alreadyAttending = set()
	for attendee in existingAttendees:
		alreadyAttending.add(attendee.attendee_id)

	print newAttending

	toDel = alreadyAttending.intersection(newAttending)
	toIns = newAttending.difference(alreadyAttending)


	print toDel
	print "toIns:"
	print toIns

	for value in toDel:
		delResults = db.session.query(SmallGroupEventAttendance).filter_by(small_group_event_id=event).filter_by(attendee_id=value)
		for result in delResults:
			db.session.delete(result)
	for value in toIns:
		tempAttendance = SmallGroupEventAttendance(event_id=event, attendee_id=value)
		db.session.add(tempAttendance)

	db.session.commit()
	flash("You successfully saved attendance!")
	return redirect(url_for('family_group_leader_manage', fg_id=fg))

# Example of ajax route that returns JSON
@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/fun')
def fun():
	return render_template("fun/fun.html")