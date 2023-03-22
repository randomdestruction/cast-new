from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, BooleanField
from wtforms.validators import Required, Length, EqualTo
from .validators import check_username

class RegisterForm(FlaskForm):
	username = StringField('Username', validators=[Required(), Length(1, 64), check_username])
	password = PasswordField('Password', [Required(), Length(1, 128), EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')
	submit = SubmitField('Register')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[Required(), Length(1, 64)])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Login')

class ChangePasswordForm(FlaskForm):
	password = PasswordField('Current Password', validators=[])
	new_password = PasswordField('New Password', [Required(), Length(1, 128), EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat New Password')
	submit = SubmitField('Confirm')

class ChangeAvatarForm(FlaskForm):
	avatar_url = StringField('Avatar URL', validators=[Required()])
	submit = SubmitField('Confirm')

class AdminToggleForm(FlaskForm):
	admin = BooleanField('Admin')
	submit = SubmitField('Do')
