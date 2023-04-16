from wtforms import Form, StringField, TextAreaField


class ProfileForm(Form):
    nick = TextAreaField('Nick')