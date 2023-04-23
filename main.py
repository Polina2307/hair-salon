from multiprocessing import Process

from app import app
from data import db_session
from employee.blueprint import employee
from profile.blueprint import profile
from timetable.blueprint import timetable
from bot.main import run_pooling


import view

# app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

app.register_blueprint(employee, url_prefix='/employee')
app.register_blueprint(profile, url_prefix='/profile')
app.register_blueprint(timetable, url_prefix='/timetable')
db_session.global_init("db/hair_salon.sqlite")


@app.get(rule='/start_bot')
def start_bot():
    bot_process = Process(target=run_pooling)
    bot_process.start()

    return str(bot_process.pid)


def main():
    app.run()


if __name__ == '__main__':
    main()
