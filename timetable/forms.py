from wtforms import Form, StringField, DateField, SelectField
from data.employee import Employee


def list_employee():
    return Employee.query.all()


class TimetableForm(Form):
    date = DateField('Дата')
    employee_id = SelectField('Мастер', choices=[])
    reception_time_id = SelectField('Время', choices=[])
