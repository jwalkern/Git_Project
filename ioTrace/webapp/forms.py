from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired, Email, ValidationError
from webapp.models import User, Device


class CreateDeviceForm(FlaskForm):
    devicename = StringField('Device Name', validators=[DataRequired(), Length(min=0, max=20)])
    devicetype = SelectField('Device Type', choices=[('s1','Sensor1'),('s2','Sensor2'),('s3','Sensor3'),('track','Tracker'),('track+','Tracker +')], validators=[DataRequired()])
    submit = SubmitField('Create Device')
    
class GenerateDummyData(FlaskForm):
    device_uid = IntegerField('Device UID', validators=[InputRequired()])
    submit = SubmitField('Generate Dummy Data!')
    
    def validate_device(self, device_uid):
        device = Device.query.filter_by(id=device_uid.data).first()
        if not device:
            raise ValidationError("The device id is not created, please submit a corresponded ID!")
    

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken. Please choose a different one.')    
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Account Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken. Please choose a different one.')  