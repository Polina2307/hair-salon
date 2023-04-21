import sqlalchemy

from data.db_session import SqlAlchemyBase


class Employee(SqlAlchemyBase):
    __tablename__ = 'employee'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(20))
    surname = sqlalchemy.Column(sqlalchemy.String(30))
    middle_name = sqlalchemy.Column(sqlalchemy.String(30))

    def __str__(self):
        return f"{self.surname} {self.name} {self.middle_name}"
