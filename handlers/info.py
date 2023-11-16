from funcs.users import CheckUser
from funcs import dt, deposit, users, payments
from messages.info import info_deposit, info_pay
from keyboards.inline import menu as kb_menu

from aiogram import F, Router
from aiogram.types import CallbackQuery


router_info = Router()


@router_info.callback_query(CheckUser(), F.data == 'menu_check_deposit')
async def show_info_deposit(callback: CallbackQuery):
    uid = users.get_uid_from_tid(callback.from_user.id)
    last_pay = payments.get_last_pay(uid)
    next_pay = payments.get_next_date_pay(uid)
    await callback.answer()
    await callback.message.answer(info_deposit % (
        dt.get_now()[2],
        "%.2f" % float(deposit.get_deposit(uid)),
        next_pay[0] if next_pay != -1 else '*',
        next_pay[1] if next_pay != -1 else '*',
        dt.conv_format(last_pay['date']) if last_pay is not None else 'Нет информации',
        "%.2f" % float(last_pay['sum']) if last_pay is not None else 'Нет информации',
        last_pay['ext_id'] if last_pay['ext_id'] != '' else last_pay['dsc']
    ), reply_markup=kb_menu.kb_menu)


@router_info.callback_query(CheckUser(), F.data == 'menu_pay')
async def show_info_pay(callback: CallbackQuery):
    await callback.answer()
    uid = users.get_uid_from_tid(callback.from_user.id)
    user_passwd = users.get_user_password(uid)
    await callback.message.answer(info_pay % (
        user_passwd['login'], user_passwd['password']
    ), reply_markup=kb_menu.kb_menu)
