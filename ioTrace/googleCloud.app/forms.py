from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo
from email_validator import validate_email

class CreateDeviceForm(FlaskForm):
    deviceName = StringField('deviceName', validators=[DataRequired(), Length(min=0, max=20)])
    userID = IntegerField('userID', validators=[InputRequired()])
    create = SubmitField('Create Device')
    
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    #validate_email(str(email))
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')
    #validate_email(str(email))