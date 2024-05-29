from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager, StartMode

from tgbot.database.orm_query import check_superadmin, get_admins, orm_add_users, remove_admin
from tgbot.dialogs.states import Menu, AdminPanel
from tgbot.kbd.keyboards import admin_list
from tgbot.utils.logger_config import logging


start_router = Router()
handlers_logger = logging.getLogger('code_logger')


@start_router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager, session: AsyncSession):
    data = {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name
    }
    await orm_add_users(session, data)
    await dialog_manager.start(state=Menu.start, mode=StartMode.RESET_STACK)


@start_router.message(Command('admin'))
async def start_admin_dialog(message: Message, dialog_manager: DialogManager):
    chat_id = message.from_user.id
    if await check_superadmin(chat_id):
        await dialog_manager.start(state=AdminPanel.start)


async def callback_delete_admin(callback: CallbackQuery, dialog_manager: DialogManager):
    session: AsyncSession = dialog_manager.middleware_data.get('session')
    user_id = callback.data.split(':')[1]
    await remove_admin(user_id, session)
    await callback.message.answer('Пользователь был успешно удален из администраторов.')
    await callback.answer()


@start_router.callback_query(F.data.startswith('delete_admin:'))
async def callback_delete_admin(callback: CallbackQuery, session: AsyncSession, dialog_manager: DialogManager):
    user_id = callback.data.split(':')[-1]
    await remove_admin(user_id, session)
    admins_db = await get_admins(session)
    keyboard = admin_list(admins_db)
    await callback.message.edit_text(
        f'Пользователь {user_id} был успешно удален из администраторов.', reply_markup=keyboard)
    await callback.answer()
