from wtforms import Form, StringField


class EmployeeForm(Form):
    surname = StringField('Фамилия')
    name = StringField('Имя')
    middle_name = StringField('Отчество')
