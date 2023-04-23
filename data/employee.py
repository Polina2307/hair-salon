from typing import Optional

from aiogram.types import InlineKeyboardButton as Button
from aiogram.types import InlineKeyboardMarkup as Markup
from aiogram.types import Message

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from data.db_session import SqlAlchemyBase
from data import db_session


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

    @classmethod
    def message_emp(cls, new_message: Message):
        """Сообщение со списком мастеров"""
        markup: Optional[Markup] = Markup()
        db_sess = db_session.create_session()
        employees = db_sess.query(Employee).all()
        for employee in employees:
            markup.row(Button(text=f"{employee.surname} {employee.name}", callback_data=f"emp_{employee.id}"))
        markup.row(Button(text="⤴️назад", callback_data=f"записаться"))
        new_message.reply_markup = markup
