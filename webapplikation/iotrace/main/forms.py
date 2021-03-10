from flask_wtf import FlaskForm
from wtforms import SubmitField

class GenerateDummyData(FlaskForm):
	"""Generate dummy data!
	
	[DELETE THIS]
	
	Extends:
		FlaskForm
	
	Variables:
		submit {[type]} -- [description]
	"""
    submit = SubmitField('Generate Dummy Data!')