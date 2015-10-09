from datetime import datetime
import os
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship, synonym, backref

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


yearMap = {
	1: "freshman",
	2: "sophomore",
	3: "junior",
	4: "senior",
	5: "other"
}

invertYearMap = { v: k for k, v in yearMap.items()}

""" User """
class User(Base):
	__tablename__ = 'leader'

	id = Column(Integer, primary_key=True)
	name = Column(String(200))
	password = Column(String(100))
	scope = Column(Integer)

	def __init__(self, name, password, scope):
		self.name = name
		self.password = password
		self.scope = scope

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % self.name

""" Large group """
class LargeGroup(Base):
	__tablename__ = 'large_group'

	id = Column(Integer, primary_key=True)
	weekNumber = Column(Integer)
	quarter = Column(String(10))
	name = Column(String(200))
	date = Column(DateTime, default=datetime.utcnow())

""" Small group """ 
class SmallGroup(Base):
	__tablename__ = 'small_group'

	id = Column(Integer, primary_key=True)
	name = Column(String(200))

	leader_id = Column(Integer, ForeignKey('leader.id'))
	leader = relationship("User", backref=backref('small_groups', order_by=id))


""" Small Group Event Class """
class SmallGroupEvent(Base):
	__tablename__ = 'small_group_event'

	id = Column(Integer, primary_key=True)
	name = Column(String(200))
	description = Column(String(500))
	weekNumber = Column(Integer)
	quarter = Column(String(10))

	small_group_id = Column(Integer, ForeignKey('small_group.id'))
	small_group = relationship("SmallGroup", backref=backref('small_group_events', order_by=id))


""" Attendeee Class """
class Attendee(Base):
	__tablename__ = 'attendee'

	id = Column(Integer, primary_key=True)
	first_name = Column(String(200))
	last_name = Column(String(200))
	year = Column(String(200))
	email = Column(String(100), unique=True)
	dorm = Column(String(100))
	temp = "test"

	def __init__(self, first_name, last_name, year, email, dorm):
		self.first_name = first_name
		self.last_name = last_name
		self.year = year
		self.email = email
		self.dorm = dorm

	def __repr__(self):
		return '<Attendee %r>' % self.first_name

""" Large Group Attendance Class """
class LargeGroupAttendance(Base):
	__tablename__ = 'large_group_attendance'

	id = Column(Integer, primary_key=True)
	first_time = Column(Integer)

	large_group_id = Column(Integer, ForeignKey('large_group.id'))
	large_group = relationship("LargeGroup", backref=backref('large_group_attendance', order_by=id))

	attendee_id = Column(Integer, ForeignKey('attendee.id'))
	attendee = relationship("Attendee", backref=backref('large_group_attendance', order_by=id))

""" Small Group Event Attendance Class """
class SmallGroupEventAttendance(Base):
	__tablename__ = 'small_group_event_attendance'

	id = Column(Integer, primary_key=True)

	small_group_event_id = Column(Integer, ForeignKey('small_group_event.id'))
	small_group_event = relationship("SmallGroupEvent", backref=backref('small_group_event_attendance', order_by=id))

	attendee_id = Column(Integer, ForeignKey('attendee.id'))
	attendee = relationship("Attendee", backref=backref('small_group_event_attendance', order_by=id))

	def __init__(self, event_id, attendee_id):
		self.small_group_event_id = event_id
		self.attendee_id = attendee_id

if __name__ == '__main__':
	from sqlalchemy import create_engine
	from sqlalchemy.orm import sessionmaker

	PWD = os.path.abspath(os.curdir)

	#SQLALCHEMY_DATABASE_URI = 'postgres://PhilipHouse:house@localhost/arkaios'
	SQLALCHEMY_DATABASE_URI = 'postgres://gtwnxaeulqztlh:Af5wrfurq510fqonyoFiZryaFg@ec2-54-197-241-91.compute-1.amazonaws.com:5432/d5uaju8veb38j0'

	#location = os.environ['DATABASE_URL']
	location = SQLALCHEMY_DATABASE_URI

	engine = create_engine(location, echo=True)

	#Base.metadata.create_all(engine)
	Session = sessionmaker(bind=engine)
	session = Session()

	# # Add a sample user
	# user = User(name='Philip House', password="test", scope=int(0))
	# largegroup = LargeGroup(name='TestFocus', weekNumber=1, quarter="w14")
	# session.add(largegroup)
	# session.add(user)
	# session.commit()

	# DO NOT RUN IF YOU DON"T WANT TO INCREMENT YEAR PLEASE

	attendees = session.query(Attendee).all()
	print attendees
	failure = False
	for attendee in attendees:
		if failure:
			break
		try:
			if attendee.year in invertYearMap:
				# valid key, proceed normally
				currentInt = int(invertYearMap[attendee.year])
				currentInt += 1

				if currentInt in yearMap:
					print yearMap[currentInt]
					attendee.year = yearMap[currentInt]
				else:
					attendee.year = 'other'
			else:
				attendee.year = 'other'
		except Exception as e:
			print e
			failure = True

	if not failure:
		session.commit()
	else:
		print "failure"