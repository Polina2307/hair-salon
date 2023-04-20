from wtforms import Form, StringField, TextAreaField


class ProfileForm(Form):
    name = TextAreaField('Name')