import asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling
from dotenv import dotenv_values

from bot.handlers import register_handlers_menu


config = dotenv_values(".env")

API_TOKEN = config.get("BOT_TOKEN", "???")
loop = asyncio.get_event_loop()
bot = Bot(token=API_TOKEN, loop=loop, parse_mode=ParseMode.HTML)
dispatcher = Dispatcher(bot, storage=MemoryStorage())


async def on_startup(dp):
    """Срабатывает при запуске бота"""
    register_handlers_menu(dp)


async def on_shutdown(dp):
    """Запускается при остановке бота"""
    await bot.close()
    await dp.storage.close()
    await dp.storage.wait_closed()


def run_pooling():
    """Запуск бота в режиме pooling"""
    start_polling(dispatcher=dispatcher, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
