from datetime import datetime
import os
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship, synonym, backref

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

""" User """
class User(Base):
	__tablename__ = 'leader'

	id = Column(Integer, primary_key=True)
	name = Column(String(200))
	password = Column(String(100))

	def __init__(self, name, password):
		self.name = name
		self.password = password

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
	from datetime import timedelta

	from sqlalchemy import create_engine
	from sqlalchemy.orm import sessionmaker

	PWD = os.path.abspath(os.curdir)

	SQLALCHEMY_DATABASE_URI = 'postgres://PhilipHouse:house@localhost/arkaios'
	#location = os.environ['DATABASE_URL']
	location = SQLALCHEMY_DATABASE_URI

	engine = create_engine(location, echo=True)

	Base.metadata.create_all(engine)
	Session = sessionmaker(bind=engine)
	session = Session()

	# Add a sample user
	user = User(name='Philip House', password="test")
	largegroup = LargeGroup(name='TestFocus', weekNumber=1, quarter="w14")
	session.add(largegroup)
	session.add(user)
	session.commit()