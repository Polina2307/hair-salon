from flask import Blueprint, redirect, url_for
from flask import render_template
from flask import request

from data import db_session
from data.employee import Employee
from employee.forms import EmployeeForm

employee = Blueprint('employee', __name__, template_folder='templates')  # Экземпляр класса


@employee.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        middle_name = request.form['middle_name']
        try:
            new_employee = Employee(name=name, surname=surname, middle_name=middle_name)
            db_sess = db_session.create_session()
            db_sess.add(new_employee)
            db_sess.commit()
            return redirect(url_for('employee.index'))
        except Exception as err:
            print(err)

    form = EmployeeForm()
    return render_template('employee/create.html', form=form)


@employee.route('/edit/<int:pk>', methods=['POST', 'GET'])
def edit(pk):
    db_sess = db_session.create_session()
    now_employee = db_sess.query(Employee).filter(Employee.id == pk).first()
    if request.method == 'POST':
        form = EmployeeForm(formdata=request.form, obj=now_employee)
        form.populate_obj(now_employee)
        db_sess.commit()
        return redirect(url_for('employee.index'))
    form = EmployeeForm(obj=now_employee)
    return render_template('employee/edit.html', now_employee=now_employee, form=form)


@employee.route('/')
def index():
    db_sess = db_session.create_session()
    employees = db_sess.query(Employee).all()
    return render_template('employee/index.html', obj=employees)
