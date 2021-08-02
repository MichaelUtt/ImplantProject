from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, RadioField, \
    FormField, widgets
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
import datetime
from dateutil.relativedelta import relativedelta
from app.databaseAccessors import getImplants, getCaps, getParts

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class ElementSelectorForm(FlaskForm):
    options = SelectMultipleField('OptionField', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    test = FormField(ElementSelectorForm)
    submit = SubmitField('Sign In')





class ReportForm(FlaskForm):
    today = datetime.datetime.today()
    name = StringField('Patient Name')
    number = StringField('Chart #')
    doctor = StringField('Doctor')
    date = DateField('Date', default=today)
    uncoverdate = DateField('Uncover Date', default=today+relativedelta(months=6))
    singleStage = BooleanField('Single Stage', default=False)
    restoredate = DateField('Restore Date', default=today+relativedelta(months=7), id='restoreDate')

    implants = MultiCheckboxField('OptionField', choices=getImplants())

    healingcaps = MultiCheckboxField('OptionField', choices=getCaps())
    restorativeparts = MultiCheckboxField('OptionField', choices=getParts())
    details = StringField('Report')
    restore = StringField('Restore')
    anesthetic = StringField('Anesthetic')
    tolerance = StringField('Tolerance')
    rx = StringField('Prescription')

    submit = SubmitField('Submit')
