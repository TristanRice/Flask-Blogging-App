from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, Email, DataRequired
from app.models import User

class Loginform(FlaskForm):
	username    = StringField("username", validators=[DataRequired()])
	password    = PasswordField("password", validators=[DataRequired()])
	remember_me = BooleanField("remember me")
	submit      = SubmitField("Sign in")

class RegisterForm(FlaskForm):
	username    = StringField("username", validators=[DataRequired()])
	password    = PasswordField("Password", validators=[DataRequired()])
	email       = StringField("Email", validators=[DataRequired()])
	submit      = SubmitField("Register")

	def validate_username( self, username ):
		user = User.query.filter_by(username=username.data).first( )
		if user is not None:
			raise ValidationError("Please choose a different username")

	def validate_email( self, email ):
		user = User.query.filter_by(email=email.data).first( )
		if user is not None:
			raise ValidationError("Please choose a differnet email")

class BlogPostForm(FlaskForm):
	title   = StringField("Title", validators=[DataRequired()])
	content = StringField("Content", validators=[DataRequired()])
	submit  = SubmitField("Make post")

class EditProfileForm(FlaskForm):
	aboutMe = StringField("About me", validators=[DataRequired()])
	submit  = SubmitField("Update Profile", validators=[DataRequired( )])