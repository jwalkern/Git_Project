from flask_wtf import FlaskForm
from wtforms import SubmitField

class GenerateDummyData(FlaskForm):
    submit = SubmitField('Generate Dummy Data!')