from typing import Optional

from aiogram.types import InlineKeyboardButton as Button, Chat
from aiogram.types import InlineKeyboardMarkup as Markup
from aiogram.types import ReplyKeyboardMarkup as RMarkup
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
    """Ник профиля"""

    id_tg = Column(Integer)
    """id telegram (chat_id)"""

    last_message_id = Column(Integer)
    """id последнего сообщения"""

    timetables = relationship("Timetable", back_populates="profile")
    """Записи"""

    @staticmethod
    def get(chat_id: int, nick: str):
        """Возвращаем профиль (если его нет то создаем)"""
        try:
            db = db_session.create_session()
            profile = db.query(Profile).filter(Profile.id_tg == chat_id).first()
            if not profile:
                profile = Profile(nick=nick, id_tg=chat_id)
                db.add(profile)
                db.commit()
            return profile
        except Exception as error:
            print(error)

    async def answer(self, message: Message) -> None:
        """Обработка текстового сообщения от пользователя"""
        try:
            if message.text.lower() == 'записаться':
                self._recording_mode(message=message)
            elif message.text.lower() == 'мои записи':
                self._records(message=message)
            else:
                self._menu(message=message)

            await self._send(message=message)
        except Exception as err:
            print(err)

    async def click_button(self, data) -> None:
        """Нажатие кнопки в сообщении"""
        chat: Chat = Chat(id=self.id_tg)
        new_message: Message = Message(chat=chat)
        if data == 'menu':
            self._menu(message=new_message)
        elif data == 'employee':
            new_message.text = f"{self.nick}, выберите мастера"
            Employee.message_emp(message=new_message)
        elif data == 'записаться':
            self._recording_mode(message=new_message)
        elif data == 'records':
            self._records(message=new_message)

        elif len(data.split('_')) == 2:
            if data.split('_')[0] == 'emp':
                id_emp = int(data.split('_')[1])
                new_message.text = f"{self.nick}, выберите дату"
                Timetable.message_emp_date(id_emp=id_emp, message=new_message)
            elif data.split('_')[0] == 'date':
                id_tt = int(data.split('_')[1])
                new_message.text = f"{self.nick}, выберите время"
                Timetable.message_emp_date_time(id_tt=id_tt, message=new_message)
            elif data.split('_')[0] == 'time':
                id_tt = int(data.split('_')[1])
                new_message.text = f"{self.nick}, завершите запись"
                Timetable.message_emp_date_time_final(id_tt=id_tt, message=new_message)
            elif data.split('_')[0] == 'write':
                id_tt = int(data.split('_')[1])
                new_message.text = f"{self.nick}, Вы записались"
                Timetable.message_emp_date_time_write(id_tt=id_tt, profile_id=self.id, message=new_message)
            elif data.split('_')[0] == 'detail':
                id_tt = int(data.split('_')[1])
                new_message.text = f"Запись"
                Timetable.message_emp_date_time_detail(id_tt=id_tt, message=new_message)
            elif data.split('_')[0] == 'ttdel':
                id_tt = int(data.split('_')[1])
                new_message.text = f"Запись удалена"
                Timetable.message_emp_date_time_del(id_tt=id_tt, profile_id=self.id, message=new_message)

        await self._send(message=new_message)

    def _recording_mode(self, message: Message) -> None:
        """Меню выбора режима записи"""
        message.text = f"{self.nick}, выберите режим записи"
        markup: Optional[Markup] = Markup()
        markup.row(
            Button(text="Мастера", callback_data=f"employee"),
            Button(text="⤴️назад", callback_data=f"menu")
        )
        message.reply_markup = markup

    def _records(self, message: Message) -> None:
        """Список записей"""
        message.text = f"{self.nick}, Ваши записи"
        Timetable.records(profile_id=self.id, message=message)

    def _menu(self, message: Message) -> None:
        """Главное меню"""
        markup = RMarkup()
        markup.resize_keyboard = True
        markup.one_time_keyboard = True
        markup.row_width = 2
        buttons = ['Записаться', 'Мои записи']
        markup.add(*buttons)
        message.reply_markup = markup
        message.text = f"{self.nick}, привет"

    async def _send(self, message: Message) -> None:
        """Отправляем сообщение"""
        try:
            send_message: Message = await message.answer(text=message.text, reply_markup=message.reply_markup)
            if self.last_message_id:
                await self._delete_last_message()
            self._set_message_last_id(message_id=send_message.message_id)

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

    def _set_message_last_id(self, message_id: int) -> None:
        """Вносим id последнего сообщения"""
        self.last_message_id = message_id
        try:
            db = db_session.create_session()
            profile = db.query(Profile).get(self.id)
            profile.last_message_id = message_id
            db.commit()
        except Exception as error:
            print(error)
