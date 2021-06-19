from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , BooleanField, FloatField, SelectField
from wtforms.validators import DataRequired, ValidationError, DataRequired, Email, EqualTo
from wtforms.fields.html5 import DateField
from app import db
from app.models import User

class LoginForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	password = PasswordField('Password',validators=[DataRequired()])
	submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
	name = StringField('Full Name', validators=[DataRequired()])
	weight = FloatField('Weight in Kgs', validators=[DataRequired()])
	height = FloatField('Height in centimeters', validators=[DataRequired()])
	dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
	gender = SelectField('Gender', choices=[('M', 'Male'), ('F','Female'), ('O', 'Other')], validators=[DataRequired()])
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	activity_f = SelectField('Activity Factor', choices=[('1.2', 'Sedentary(little or no exercise)'), ('1.375','Light(light exercise/sports 1-3 days/week)'), ('1.55', 'Moderate(moderate exercise/sports 3-5 days/week)'), ('1.725', 'Heavy(hard exercise/sports 6-7 days a week)'), ('1.9', 'Very Heavy(very hard exercise/sports or physical job)')], validators=[DataRequired()])
	

	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def validate_email(self,email):
		user=User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')

class Recipe(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	
class EditProfileForm(FlaskForm):
	name = StringField('Full Name', validators=[DataRequired()])
	weight = FloatField('Weight in Kgs', validators=[DataRequired()])
	height = FloatField('Height in centimeters', validators=[DataRequired()])
	dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
	gender = SelectField('Gender', choices=[('M', 'Male'), ('F','Female'), ('O', 'Other')], validators=[DataRequired()])
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	activity_f = SelectField('Activity Factor', choices=[('1.2', 'Sedentary(little or no exercise)'), ('1.375','Light(light exercise/sports 1-3 days/week)'), ('1.55', 'Moderate(moderate exercise/sports 3-5 days/week)'), ('1.725', 'Heavy(hard exercise/sports 6-7 days a week)'), ('1.9', 'Very Heavy(very hard exercise/sports or physical job)')], validators=[DataRequired()])

	submit = SubmitField('Save')

	def __init__(self, original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError('Please use a different username.')