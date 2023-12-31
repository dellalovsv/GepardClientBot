from config import Telegram

from handlers import start, info

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


async def main():
    bot = Bot(token=Telegram.token, parse_mode='HTML')
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        start.routers_start,
        info.router_info,
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit...')
