from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, MacAddress, ValidationError
from iotrace.models import Xtel, Device




class CreateDeviceForm(FlaskForm):
	device_mac = StringField('Device Mac Address', validators=[MacAddress()], render_kw={"placeholder": "00:00:00:00:00:00"})
	devicename = StringField('Device Name', validators=[DataRequired(), Length(min=0, max=20)], render_kw={"placeholder": "Please enter a name"})
	submit = SubmitField('Create Device')

	def validate_device_mac(self, device_mac):
		macaddr = Device.query.filter_by(device_mac=device_mac.data).first()
		if macaddr:
			raise ValidationError('Mac address is used by others.')
		device = Xtel.query.filter_by(device_mac=device_mac.data).first()
		if not device:
			raise ValidationError('The Mac Address is invalid. Please check or contact support.')

class EditDeviceForm(FlaskForm):
	devicename = StringField('Device Name', validators=[DataRequired(), Length(min=0, max=20)])
	mintemp = IntegerField('Device Min Temp', render_kw={"placeholder": "min temp"})
	maxtemp = IntegerField('Device Max Temp', render_kw={"placeholder": "max temp"})
	minhumid = IntegerField('Device Min Humid', render_kw={"placeholder": "min humid"})
	maxhumid = IntegerField('Device Max Humid', render_kw={"placeholder": "max humid"})
	minhpa = IntegerField('Device Min Hpa', render_kw={"placeholder": "min hpa"})
	maxhpa = IntegerField('Device Max Hpa', render_kw={"placeholder": "max hpa"})
	submit = SubmitField('Apply Value')