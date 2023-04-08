from app import app
from data import db_session

# app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/hair_salon.sqlite")
    app.run()


if __name__ == '__main__':
    main()
