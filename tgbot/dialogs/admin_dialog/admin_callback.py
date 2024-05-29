from aiogram.types import CallbackQuery, Message
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager

from tgbot.utils.download import download_xlsx
from tgbot.database.orm_query import add_admin, get_admins
from tgbot.kbd.keyboards import admin_list


async def download_report(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
):
    await download_xlsx(callback=callback, dialog_manager=dialog_manager)
    await dialog_manager.done()


async def delete_admin(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
):
    session = dialog_manager.middleware_data.get('session')
    admins_db = await get_admins(session)
    if admins_db == []:
        await callback.answer('Список администраторов пуст.', show_alert=True)
        return
    keyboard = admin_list(admins_db)

    await callback.message.answer('Выберите пользователя для удаления', reply_markup=keyboard)
    await callback.answer()


async def add_admin_input(message: Message, button: Button, dialog_manager: DialogManager):
    session = dialog_manager.middleware_data.get('session')

    message_text = message.text.strip()

    if message_text.isdigit():
        user_id = int(message_text)
        username = None
    else:
        user_id = None
        username = str(message_text)

    result = await add_admin(session, message, user_id=user_id, username=username)
    if result is None:
        await message.answer(f'Пользователь <b>{message_text}</b> не найден.')
        return

    await message.answer(f'Пользователь <b>{message_text}</b> был успешно добавлен в администраторы.')

    await dialog_manager.back()
