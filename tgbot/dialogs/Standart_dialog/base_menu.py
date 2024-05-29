from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Column, Start, Url, Group
from aiogram_dialog.widgets.text import Format, Const



from tgbot.dialogs.states import Menu, AdminPanel, Survay
from tgbot.dialogs.getters import (
    username_getter,
)


start_dialog = Dialog(
    Window(
        Format('{hello_user}'),
        Group(
            Column(
                Start(
                    Format(text='{rate_btn}'),
                    id='go_to_survay',
                    state=Survay.start
                )
            ),
            Column(
                Url(
                    Format(text='{url_button}'),
                    url=Const('https://kwork.ru/seller'),
                    id='go_to_doctor'
                )
            )
        ),
        Column(
            Start(
                text=Const('Админ панель'),
                id='start_admin_pnl',
                when='is_admin',
                state=AdminPanel.start
            )
        ),
        state=Menu.start,
        getter=username_getter,
    ),
)
