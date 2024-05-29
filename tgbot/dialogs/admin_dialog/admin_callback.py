from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager

from tgbot.utils.download import download_xlsx
from tgbot.database.orm_query import get_admins
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
    keyboard = admin_list(admins_db)

    await callback.message.answer('Выберите пользователя для удаления', reply_markup=keyboard)
    await callback.answer('')
