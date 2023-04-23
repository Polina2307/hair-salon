from _datetime import datetime
from typing import Optional

import sqlalchemy
from aiogram.types import InlineKeyboardButton as Button
from aiogram.types import InlineKeyboardMarkup as Markup
from aiogram.types import Message
from sqlalchemy import Column, Integer, ForeignKey, Date, String
from sqlalchemy.orm import relationship

from data import db_session
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

    @classmethod
    def message_emp_date(cls, id_emp: int, new_message: Message):
        """Формирование дат по конкретному мастеру"""
        markup: Optional[Markup] = Markup()
        db_sess = db_session.create_session()
        date_today = datetime.today().date()
        timetables = db_sess.query(Timetable).filter(Timetable.date >= date_today, Timetable.profile_id == None).filter(
            Timetable.employee_id == id_emp).order_by(Timetable.date).all()
        timetables_dict = dict()

        for timetable in timetables:
            timetables_dict[str(timetable.date)] = timetable.id
        for key, value in timetables_dict.items():
            markup.row(Button(text=str(key), callback_data=f"date_{value}"))
        markup.row(Button(text="⤴️назад", callback_data=f"employee"))
        new_message.reply_markup = markup

    @classmethod
    def message_emp_date_time(cls, id_tt: int, new_message: Message):
        """Формирование свободных часов на конкретную лату конкретного мастера"""
        markup: Optional[Markup] = Markup()
        db_sess = db_session.create_session()
        timetable: Timetable = db_sess.query(Timetable).get(id_tt)
        timetables = db_sess.query(Timetable).filter(Timetable.date == timetable.date,
                                                     Timetable.employee_id == timetable.employee_id,
                                                     Timetable.profile_id == None).order_by(Timetable.id).all()
        for timetable in timetables:
            markup.row(Button(text=timetable.reception_time.time, callback_data=f"time_{timetable.reception_time_id}"))
        markup.row(Button(text="⤴️назад", callback_data=f"employee"))
        new_message.reply_markup = markup


class ReceptionTime(SqlAlchemyBase):
    """Время приема"""
    __tablename__ = 'reception_time'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = sqlalchemy.Column(String)

    timetables = relationship("Timetable", back_populates="reception_time", cascade="all, delete-orphan")
