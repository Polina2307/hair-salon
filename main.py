from app import app
from data import db_session
from employee.blueprint import employee
from profile.blueprint import profile


import view

# app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

app.register_blueprint(employee, url_prefix='/employee')
app.register_blueprint(profile, url_prefix='/profile')


def main():
    db_session.global_init("db/hair_salon.sqlite")
    app.run()


if __name__ == '__main__':
    main()
