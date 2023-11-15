from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


kb_phones = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text='Отправить № телефона', request_contact=True)]
])
