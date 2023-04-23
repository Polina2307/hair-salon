from typing import Optional

from aiogram.types import InlineKeyboardButton as Button, Chat
from aiogram.types import InlineKeyboardMarkup as Markup
from aiogram.types import Message
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from data import db_session
from data.db_session import SqlAlchemyBase
from data.employee import Employee
from data.timetable import Timetable


class Profile(SqlAlchemyBase):
    """Пользователь телеграмм"""
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nick = Column(String(20))
    id_tg = Column(Integer)
    last_message_id = Column(Integer)

    timetables = relationship("Timetable", back_populates="profile")

    @staticmethod
    def get(chat_id: int, nick: str):
        """Возвращаем профиль (если его нет то создаем)"""

        try:
            db = db_session.create_session()
            profile = db.query(Profile).first()
            if not profile:
                profile = Profile(nick=nick, id_tg=chat_id)
                db.add(profile)
                db.commit()  # сохраняем изменения
            return profile
        except Exception as error:
            print(error)

    def recording_mode(self, message: Message):
        """Меню выбора режима записи"""
        message.text = f"{self.nick}, выберите режим записи"
        markup: Optional[Markup] = Markup()
        markup.row(
            Button(text="Мастера", callback_data=f"employee")
        )
        message.reply_markup = markup

    async def click_button(self, data):
        """Нажатие кнопки в сообщении"""
        chat: Chat = Chat(id=self.id_tg)
        new_message: Message = Message(chat=chat)
        if data == 'employee':
            new_message.text = f"{self.nick}, выберите мастера"
            Employee.message_emp(new_message=new_message)
        elif data == 'записаться':
            self.recording_mode(message=new_message)

        elif len(data.split('_')) == 2:
            if data.split('_')[0] == 'emp':
                id_emp = int(data.split('_')[1])
                new_message.text = f"{self.nick}, выберите дату"
                Timetable.message_emp_date(id_emp=id_emp, new_message=new_message)
            elif data.split('_')[0] == 'date':
                id_tt = int(data.split('_')[1])
                new_message.text = f"{self.nick}, выберите время"
                Timetable.message_emp_date_time(id_tt=id_tt, new_message=new_message)

        await self.send(message=new_message)

    async def send(self, message: Message) -> None:
        """Отправляем сообщение"""
        try:
            send_message: Message = await message.answer(text=message.text, reply_markup=message.reply_markup)
            if self.last_message_id:
                await self._delete_last_message()
            self.set_message_last_id(message_id=send_message.message_id)

        except Exception as error:
            print(error)

    async def _delete_last_message(self) -> None:
        """Удаляет сообщение по его id"""
        try:
            chat: Chat = Chat(id=self.id_tg)
            message: Message = Message(chat=chat, message_id=self.last_message_id)
            await message.delete()
        except Exception as error:
            print(error)

    def set_message_last_id(self, message_id: int) -> None:
        """Вносим id последнего сообщения"""
        self.last_message_id = message_id
        try:
            db = db_session.create_session()
            profile = db.query(Profile).get(self.id)
            profile.last_message_id = message_id
            db.commit()
        except Exception as error:
            print(error)
