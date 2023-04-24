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
    """Дата в расписании"""

    employee_id = Column(Integer, ForeignKey("employee.id"))
    """id мастера"""

    employee = relationship("Employee", back_populates="timetables")
    """Мастер"""

    reception_time_id = Column(Integer, ForeignKey("reception_time.id"))
    """id времени"""

    reception_time = relationship("ReceptionTime", back_populates="timetables")
    """Время в расписании"""

    profile_id = Column(Integer, ForeignKey("profile.id"))
    """id профиля"""

    profile = relationship("Profile", back_populates="timetables")
    """Профиль"""

    @classmethod
    def new_sess_markup(cls) -> tuple:
        """Формируем новое подключение к бд и новую клавиатуру"""
        markup: Optional[Markup] = Markup()
        db_sess = db_session.create_session()
        return markup, db_sess

    @classmethod
    def message_emp_date(cls, id_emp: int, message: Message) -> None:
        """Формирование дат по конкретному мастеру"""
        markup, db_sess = cls.new_sess_markup()
        date_today = datetime.today().date()
        timetables = db_sess.query(Timetable).filter(Timetable.date >= date_today).filter(
            Timetable.profile_id == None).filter(Timetable.employee_id == id_emp).order_by(Timetable.date).all()
        timetables_dict = dict()

        for timetable in timetables:
            timetables_dict[str(timetable.date)] = timetable.id
        for key, value in timetables_dict.items():
            markup.row(Button(text=str(key), callback_data=f"date_{value}"))
        markup.row(Button(text="⤴️назад", callback_data=f"employee"))
        message.reply_markup = markup

    @classmethod
    def message_emp_date_time(cls, id_tt: int, message: Message) -> None:
        """Формирование свободных часов на конкретную лату конкретного мастера"""
        markup, db_sess = cls.new_sess_markup()
        timetable: Timetable = db_sess.query(Timetable).get(id_tt)
        timetables = db_sess.query(Timetable).filter(Timetable.date == timetable.date).filter(
            Timetable.employee_id == timetable.employee_id).filter(
            Timetable.profile_id == None).order_by(Timetable.id).all()
        for timetable in timetables:
            markup.row(Button(text=timetable.reception_time.time, callback_data=f"time_{timetable.id}"))
        markup.row(Button(text="⤴️назад", callback_data=f"employee"))
        message.reply_markup = markup

    @classmethod
    def message_emp_date_time_final(cls, id_tt: int, message: Message) -> None:
        """Формирование финального сообщения о записи"""
        markup, db_sess = cls.new_sess_markup()
        timetable: Timetable = db_sess.query(Timetable).get(id_tt)
        message.text += f"\n <b>Мастер: </b>{timetable.employee}\n" \
                            f"<b>Дата: </b>{timetable.date}\n" \
                            f"<b>Время: </b>{timetable.reception_time.time}"
        markup.row(
            Button(text="записаться", callback_data=f"write_{timetable.id}"),
            Button(text="⤴️назад", callback_data=f"date_{timetable.id}")
        )
        message.reply_markup = markup

    @classmethod
    def message_emp_date_time_write(cls, id_tt: int, profile_id: int, message: Message) -> None:
        """Сохранение записи"""
        markup, db_sess = cls.new_sess_markup()
        timetable: Timetable = db_sess.query(Timetable).get(id_tt)
        timetable.profile_id = profile_id
        db_sess.commit()
        markup.row(
            Button(text="⤴️назад", callback_data=f"menu")
        )
        message.reply_markup = markup

    @classmethod
    def message_emp_date_time_detail(cls, id_tt: int, message: Message) -> None:
        """Детали записи"""
        markup, db_sess = cls.new_sess_markup()
        timetable: Timetable = db_sess.query(Timetable).get(id_tt)
        message.text += f"\n <b>Мастер: </b>{timetable.employee}\n" \
                            f"<b>Дата: </b>{timetable.date}\n" \
                            f"<b>Время: </b>{timetable.reception_time.time}"
        markup.row(
            Button(text="удалить", callback_data=f"ttdel_{timetable.id}"),
            Button(text="⤴️назад", callback_data=f"records")
        )
        message.reply_markup = markup

    @classmethod
    def message_emp_date_time_del(cls, id_tt: int, profile_id: int, message: Message) -> None:
        """Удаление записи"""
        markup, db_sess = cls.new_sess_markup()
        timetable: Timetable = db_sess.query(Timetable).get(id_tt)
        timetable.profile_id = None
        db_sess.commit()
        cls.records(profile_id=profile_id, message=message)

    @classmethod
    def records(cls, profile_id: int,  message: Message) -> None:
        """Список записей"""
        markup, db_sess = cls.new_sess_markup()
        date_today = datetime.today().date()
        timetables = db_sess.query(Timetable).filter(Timetable.date >= date_today).filter(
            Timetable.profile_id == profile_id).order_by(Timetable.date).all()
        for timetable in timetables:
            markup.row(Button(
                text=f"{timetable.date} {timetable.employee.surname} "
                     f"{timetable.employee.name} {timetable.reception_time.time}",
                callback_data=f"detail_{timetable.id}"))
        if not timetables:
            message.text += "\nУ Вас нет активных записей!"
        markup.row(Button(text="⤴️назад", callback_data=f"menu"))
        message.reply_markup = markup


class ReceptionTime(SqlAlchemyBase):
    """Время приема"""
    __tablename__ = 'reception_time'

    id = Column(Integer, primary_key=True, autoincrement=True)

    time = sqlalchemy.Column(String)
    """Время записи"""

    timetables = relationship("Timetable", back_populates="reception_time", cascade="all, delete-orphan")
