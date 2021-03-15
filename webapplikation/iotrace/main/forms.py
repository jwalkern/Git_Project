from flask_wtf import FlaskForm
from wtforms import SubmitField

class GenerateTrackingDeviceData(FlaskForm):
    submit = SubmitField('Generate Dummy Data!')