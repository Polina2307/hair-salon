import sqlalchemy

from data.db_session import SqlAlchemyBase


class Profile(SqlAlchemyBase):
    __tablename__ = 'profile'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    nick = sqlalchemy.Column(sqlalchemy.String(20))
    id_tg = sqlalchemy.Column(sqlalchemy.Integer)
