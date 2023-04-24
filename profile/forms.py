from wtforms import Form, TextAreaField


class ProfileForm(Form):
    name = TextAreaField('Name')
