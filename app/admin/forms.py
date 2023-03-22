from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required

class AnnouncementForm(FlaskForm):
	message = StringField('Message', validators=[Required()])
	submit = SubmitField('Submit')

class PickUserForm(FlaskForm):
	user = SelectField('User', coerce=int, validators=[Required()])
	submit = SubmitField('Edit')
