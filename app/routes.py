from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, ReportForm
from app.models import Report, Implant, Caps, RestorativeParts
from app.databaseAccessors import getCaps, getParts, getImplants


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Michael'}
    return render_template('index.html', user=user)

@app.route('/template', methods=['GET', 'POST'])
def template():
    report = ReportForm()

    return render_template('implant_template.html', report=report)

createReportForm = None
@app.route('/create', methods=['GET', 'POST'])
def create():
    createReportForm = ReportForm()

    createReportForm.implants.choices = getImplants()
    createReportForm.healingcaps.choices = getCaps()
    createReportForm.restorativeparts.choices = getParts()
    if createReportForm.validate_on_submit():
        pass
    return render_template('create_report.html', form=createReportForm)

@app.route('/add_implant/<new_implant>')
def add_implant(new_implant=""):
    i = Implant(data=new_implant)
    db.session.add(i)
    db.session.commit()
    print("Committing: " + new_implant)
    return "nothing"

@app.route('/remove_implant/<old_implant>')
def remove_implant(old_implant=""):
    i = Implant.query.filter_by(data=old_implant).first()
    db.session.delete(i)
    db.session.commit()
    print("Removing: " + old_implant)
    return "nothing"

@app.route('/add_cap/<new_cap>')
def add_cap(new_cap=""):
    c = Caps(data=new_cap)
    db.session.add(c)
    db.session.commit()
    print("Committing: " + new_cap)
    return "nothing"

@app.route('/remove_cap/<old_cap>')
def remove_cap(old_cap=""):
    c = Caps.query.filter_by(data=old_cap).first()
    db.session.delete(c)
    db.session.commit()
    print("Removing: " + old_cap)
    return "nothing"

@app.route('/add_part/<new_part>')
def add_part(new_part=""):
    p = RestorativeParts(data=new_part)
    db.session.add(p)
    db.session.commit()
    print("Committing: " + new_part)
    return "nothing"

@app.route('/remove_part/<old_part>')
def remove_part(old_part=""):
    p = Caps.query.filter_by(data=old_part).first()
    db.session.delete(p)
    db.session.commit()
    print("Removing: " + old_part)
    return "nothing"

@app.route('/do_nothing')
def do_nothing():
    return "nothing"

def add_report():
    reportForm = ReportForm()
    if reportForm.validate_on_submit():
        report = Report()
        report = Report()
        formData = (
            reportForm.name.data,
            reportForm.number.data,
            reportForm.doctor.data,
            reportForm.date.data,
            reportForm.uncoverdate.data,
            reportForm.restoredate.data,

            reportForm.implants,
            reportForm.healingcaps,
            reportForm.restorativeparts,

            reportForm.details.data,
            reportForm.restore.data,
            reportForm.anesthetic.data,
            reportForm.tolerance.data,
            reportForm.rx.data
        )

def add_implant():
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    logForm = LoginForm()
    if logForm.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            logForm.username.data, logForm.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', form=logForm)

