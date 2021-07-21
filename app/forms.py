from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ReportForm(FlaskForm):
    name = StringField('Name')
    number = StringField('Chart #')
    doctor = StringField('Doctor')
    date = DateField('Date')
    uncoverdate = DateField('Uncover Date')
    restoredate = DateField('Restore Date')
    implants = []
    healingcaps = []
    restorativeparts = []
    details = StringField('Report')
    restore = StringField('Restore')
    anesthetic = StringField('Anesthetic')
    tolerance = StringField('Tolerance')
    rx = StringField('Prescription')

