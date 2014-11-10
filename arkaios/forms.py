from flask.ext.wtf import Form
from wtforms import TextField, SelectField, PasswordField
from wtforms.validators import Required

class EventForm(Form):
	name = TextField('name', validators = [Required()])
	description = TextField('description', validators = [Required()])
	quarter = SelectField('quarter', choices = [('f14', 'Fall 2014'), ('w15', 'Winter 2015'), ('s15', 'Spring 2015')], validators = [Required()])
	week = SelectField('week', choices = tuple((number, number) for number in range(1,10)), validators = [Required()], coerce=int)

class LoginForm(Form):
	username = TextField('username', validators = [Required()])
	password = PasswordField('password', validators = [Required()])

class AttendeeForm(Form):
	first_name = TextField('first name', validators = [Required()])
	last_name = TextField('last name', validators = [Required()])
	year = SelectField('year', choices = [('freshman', 'Freshman'), ('sophomore', 'Sophomore'), ('junior', 'Junior'), ('senior', 'Senior')], validators = [Required()])
	email = TextField('email', validators = [Required()])
	dorm = TextField('dorm')
	