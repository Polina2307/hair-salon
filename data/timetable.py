import sqlalchemy
from sqlalchemy import Column, Integer, ForeignKey, Date, Time
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


class ReceptionTime(SqlAlchemyBase):
    """Время приема"""
    __tablename__ = 'reception_time'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = sqlalchemy.Column(Time)

    timetables = relationship("Timetable", back_populates="reception_time", cascade="all, delete-orphan")
