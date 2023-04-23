from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup as RMarkup
from data.models import Profile


async def cmd_start(message: Message) -> None:
    """Команда старт от пользователя"""
    profile = Profile.get(chat_id=message.chat.id, nick=message.from_user.first_name)
    message.text = f"Привет, {profile.nick}"
    await answer(message=message)


async def answer(message: Message) -> None:
    """Обработка текстового сообщения от пользователя"""
    try:
        await clearing(message)
        profile = Profile.get(chat_id=message.chat.id, nick=message.from_user.first_name)
        if message.text.lower() == 'записаться':
            profile.recording_mode(message=message)
        else:
            markup = RMarkup()
            markup.resize_keyboard = True
            markup.one_time_keyboard = True
            markup.row_width = 2
            buttons = ['Записаться', 'Мои записи']
            markup.add(*buttons)
            message.reply_markup = markup
            message.text = "Привет"

        await profile.send(message=message)
    except Exception as err:
        print(err)


async def click_button(call: CallbackQuery) -> None:
    """Реакция на нажатие кнопки в сообщении"""
    try:
        # click_button_task.delay(data=call.data, chat_id=call.message.chat.id)
        profile = Profile.get(chat_id=call.message.chat.id, nick=call.message.from_user.first_name)
        await profile.click_button(data=call.data)
    except Exception as err:
        print(err)


async def clearing(message: Message) -> None:
    """Удаление сообщений и команд от пользователя."""
    try:
        await message.delete()
    except Exception as err:
        print(err)


async def send(message: Message) -> None:
    """Отправляет сообщение и возвращает его id"""
    try:
        await message.answer(text=message.text, reply_markup=message.reply_markup)
    except Exception as err:
        print(err)


def register_handlers_menu(dp: Dispatcher) -> None:
    """Регистрация обработчиков команд и сообщений от пользователя."""
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(answer)
    dp.register_callback_query_handler(click_button)
