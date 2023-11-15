from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


kb_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Проверить состояние счета', callback_data='menu_check_deposit')]
])
