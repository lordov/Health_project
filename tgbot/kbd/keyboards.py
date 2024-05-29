from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_list(admin_list: list, sizes: tuple[int] = (1,)) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for admin in admin_list:
        button = InlineKeyboardButton(
            text=f'{admin.username} ({admin.first_name} {admin.last_name})',
            callback_data=f'delete_admin:{admin.user_id}'
        )
        keyboard.add(button)
    return keyboard.adjust(*sizes).as_markup()
