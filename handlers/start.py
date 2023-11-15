from funcs import users
from messages import start as msg_start

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart


routers_start = Router()


@routers_start.message(users.CheckUser(), CommandStart)
async def start(m: Message):
    ...
