import sqlalchemy
from sqlalchemy import Column, Integer, ForeignKey, Date, Time, String
from sqlalchemy.orm import relationship

from data.db_session import SqlAlchemyBase


class Timetable(SqlAlchemyBase):
    """Расписание"""
    __tablename__ = 'timetable'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(Date)

    employee_id = Column(Integer, ForeignKey("employee.id"))
    employee = relationship("Employee", back_populates="timetables")

    reception_time_id = Column(Integer, ForeignKey("reception_time.id"))
    reception_time = relationship("ReceptionTime", back_populates="timetables")

    profile_id = Column(Integer, ForeignKey("profile.id"))
    profile = relationship("Profile", back_populates="timetables")

    # def __init__(self, employee, reception_time):
    #     self.employee = employee
    #     self.reception_time = reception_time


class ReceptionTime(SqlAlchemyBase):
    """Время приема"""
    __tablename__ = 'reception_time'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = sqlalchemy.Column(String)

    timetables = relationship("Timetable", back_populates="reception_time", cascade="all, delete-orphan")
