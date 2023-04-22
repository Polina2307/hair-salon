from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from data.db_session import SqlAlchemyBase


class Profile(SqlAlchemyBase):
    """Пользователь телеграмм"""
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nick = Column(String(20))
    id_tg = Column(Integer)

    timetables = relationship("Timetable", back_populates="reception_time")
