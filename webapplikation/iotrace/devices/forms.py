from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class CreateDeviceForm(FlaskForm):
    devicename = StringField('Device Name', validators=[DataRequired(), Length(min=0, max=20)])
    devicetype = SelectField('Device Type', choices=[('s1','Sensor1'),('s2','Sensor2'),('s3','Sensor3'),('track','Tracker'),('track+','Tracker +')], validators=[DataRequired()])
    submit = SubmitField('Create Device')
        