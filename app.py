import asyncio

from aiogram import executor

import aioschedule

from loader import dp
import handlers
from utils import kick_from_channel


async def scheduler():
    aioschedule.every().day.at('14:54').do(kick_from_channel)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
