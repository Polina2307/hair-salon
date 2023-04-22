from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from data.db_session import SqlAlchemyBase


class Employee(SqlAlchemyBase):
    """Мастер"""
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    surname = Column(String(30))
    middle_name = Column(String(30))
    timetables = relationship("Timetable", back_populates="employee", cascade="all, delete-orphan")

    def __str__(self):
        return f"{self.surname} {self.name} {self.middle_name}"
