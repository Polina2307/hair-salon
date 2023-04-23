from datetime import datetime
from tkinter.tix import Form

from flask import Blueprint, redirect, url_for
from flask import render_template
from flask import request
from wtforms import StringField, SelectField

from data import db_session
from data.timetable import Timetable
from data.employee import Employee
from timetable.forms import TimetableForm
from data.timetable import ReceptionTime


timetable = Blueprint('timetable', __name__, template_folder='templates')  # Экземпляр класса


@timetable.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], "%Y-%m-%d")
        employee_id = request.form['employee_id']
        reception_time_id = request.form['reception_time_id']
        try:
            new_timetable = Timetable(date=date, employee_id=int(employee_id), reception_time_id=int(reception_time_id))
            db_sess = db_session.create_session()
            db_sess.add(new_timetable)
            db_sess.commit()
            return redirect(url_for('timetable.index'))
        except Exception as err:
            print(err)
    db_sess = db_session.create_session()
    form = TimetableForm()
    form.reception_time_id.choices = [(x.id, x.time) for x in db_sess.query(ReceptionTime).all()]
    form.employee_id.choices = [(x.id, f"{x.surname} {x.name}") for x in db_sess.query(Employee).all()]
    return render_template('timetable/create.html', form=form)


@timetable.route('/edit/<int:pk>', methods=['POST', 'GET'])
def edit(pk):
    db_sess = db_session.create_session()
    now_timetable = db_sess.query(Timetable).filter(Timetable.id == pk).first()
    if request.method == 'POST':
        form = TimetableForm(formdata=request.form, obj=now_timetable)
        form.populate_obj(now_timetable)
        db_sess.commit()
        return redirect(url_for('timetable.index'))
    form = TimetableForm(obj=now_timetable)
    form.reception_time_id.choices = [(x.id, x.time) for x in db_sess.query(ReceptionTime).all()]
    form.employee_id.choices = [(x.id, f"{x.surname} {x.name}") for x in db_sess.query(Employee).all()]
    return render_template('timetable/edit.html', now_timetable=now_timetable, form=form)


@timetable.route('/')
def index():
    db_sess = db_session.create_session()
    timetables = db_sess.query(Timetable).all()
    return render_template('timetable/index.html', obj=timetables)

