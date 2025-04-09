# app/forms/countdown_forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateTimeLocalField

class CountdownForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    target_datetime = DateTimeLocalField('Target Date and Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    is_public = BooleanField('Make this countdown public')
    submit = SubmitField('Create Countdown')
