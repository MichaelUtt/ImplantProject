from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, ReportForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Michael'}
    return render_template('index.html', user=user)

@app.route('/template', methods=['GET', 'POST'])
def template():
    report = ReportForm()

    return render_template('implant_template.html', report=report)

@app.route('/create', methods=['GET', 'POST'])
def create():
    return render_template('create_report.html')

@app.route('/add_button')
def add_element():
    print("hello")
    return "nothing"

@app.route('/login', methods=['GET', 'POST'])
def login():
    logForm = LoginForm()
    if logForm.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            logForm.username.data, logForm.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', form=logForm)

