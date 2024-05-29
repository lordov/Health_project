from aiogram.enums import ContentType

from aiogram_dialog import Dialog,  Window
from aiogram_dialog.widgets.kbd import (
    Row,  Column,  Group, Back,
    Cancel, Button, SwitchTo
)
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import MessageInput


from tgbot.dialogs.states import Menu,  AdminPanel
from tgbot.dialogs.getters import is_superadmin
from tgbot.dialogs.admin_dialog.admin_callback import (
    download_report, delete_admin,
    add_admin_input
    )


admin_panel = Dialog(
    Window(
        Const('Админ панель: Выберите действие'),
        Group(
            Column(
                Button(
                    Const(text='Скачать отчет'),
                    id='download_report',
                    on_click=download_report
                )
            ),
            Row(
                Button(
                    Const('Удалить админа'),
                    id='del_admin',
                    when='is_super',
                    on_click=delete_admin
                ),
                SwitchTo(
                    Const('Добавить админа'),
                    id='add_admin',
                    when='is_super',
                    state=AdminPanel.add_admin
                ),
            ),
            Column(
                Cancel(
                    Const('◀️ Назад'),
                    id='cncl_adm_dialog',
                ),
            ),
        ),
        getter=is_superadmin,
        state=AdminPanel.start
    ),
    Window(
        Const('Введите id или username admina'),
        MessageInput(
            func=add_admin_input,
            content_types=ContentType.TEXT
        ),
        Column(
            Back(
                Const('◀️ Назад'),
                id='back',
            ),
        ),
        state=AdminPanel.add_admin
    )
)
