from multiprocessing import Process

from app import app
from data import db_session
from bot.main import run_pooling


import view


db_session.global_init("db/hair_salon.sqlite")


def main():
    bot_process = Process(target=run_pooling)
    bot_process.start()
    app.run()


if __name__ == '__main__':
    main()
