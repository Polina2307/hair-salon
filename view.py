from app import app
from flask import render_template

from employee.blueprint import employee
from profile.blueprint import profile
from timetable.blueprint import timetable

app.register_blueprint(employee, url_prefix='/employee')
app.register_blueprint(profile, url_prefix='/profile')
app.register_blueprint(timetable, url_prefix='/timetable')


@app.route('/')
def index():
    return render_template('home.html')
