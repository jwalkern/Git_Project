from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import  MacAddress, DataRequired, ValidationError
from iotrace.models import Device

class GenerateTrackingDeviceData(FlaskForm):
	device_mac = device_mac = StringField('Device Mac Address', validators=[MacAddress()])
	devicetype = SelectField('Device Type', choices=[('s1','Sensor1'),('s2','Sensor2'),('s3','Sensor3'),('track','Tracker'),('track+','Tracker +'),('fire','FireSensor')], validators=[DataRequired()])
	submit = SubmitField('Generate Dummy Data!')

	def validate_username(self, device_mac):
	    device = Device.query.filter_by(device_mac=device_mac.data).first()
	    if device is None:
	        raise ValidationError('No device with entered MAC address exists.')