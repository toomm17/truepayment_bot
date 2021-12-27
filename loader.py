from asyncio import get_event_loop

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from binance import AsyncClient

from data.config import BOT_TOKEN, BINANCE_API_KEY, BINANCE_SECRET_KEY
from middleware import ThrottlingMiddleware
from db import Database

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(ThrottlingMiddleware())
loop = get_event_loop()
db = loop.run_until_complete(Database.create())
client = AsyncClient(BINANCE_API_KEY, BINANCE_SECRET_KEY)

