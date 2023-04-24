from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from data.models import Profile


async def cmd_start(message: Message) -> None:
    """Команда старт от пользователя"""
    await answer(message=message)


async def answer(message: Message) -> None:
    """Обработка текстового сообщения от пользователя"""
    try:
        await clearing(message)
        profile = Profile.get(chat_id=message.chat.id, nick=message.from_user.first_name)
        await profile.answer(message=message)
    except Exception as err:
        print(err)


async def click_button(call: CallbackQuery) -> None:
    """Реакция на нажатие кнопки в сообщении"""
    try:
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


def register_handlers_menu(dp: Dispatcher) -> None:
    """Регистрация обработчиков команд и сообщений от пользователя."""
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(answer)
    dp.register_callback_query_handler(click_button)
