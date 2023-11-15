from funcs import users
from messages import start as msg_start
from keyboards.inline import menu as kb_menu

from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart


routers_start = Router()


@routers_start.message(F.contact)
async def get_phone_number(m: Message):
    uid = users.get_uid_from_phone(m.contact.phone_number)
    if uid is not None:
        if users.new_user(uid, m.from_user.id):
            await m.answer(msg_start.auth, reply_markup=ReplyKeyboardRemove())
            await m.answer(msg_start.menu_of_bot, reply_markup=kb_menu.kb_menu)
    else:
        await m.answer(msg_start.err_auth)


@routers_start.message(users.CheckUser(), CommandStart)
async def start(m: Message):
    await m.answer(msg_start.menu_of_bot, reply_markup=kb_menu.kb_menu)
