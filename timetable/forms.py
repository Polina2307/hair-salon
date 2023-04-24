from wtforms import Form, DateField, SelectField


class TimetableForm(Form):
    date = DateField('Дата')
    employee_id = SelectField('Мастер', choices=[])
    reception_time_id = SelectField('Время', choices=[])
