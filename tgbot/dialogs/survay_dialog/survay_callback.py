import re
from aiogram.types import CallbackQuery, Message
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager, ShowMode

from tgbot.dialogs.states import Survay
from tgbot.database.orm_query import (
    orm_add_info_surv,
)
from tgbot.utils.generate_text import generate_response


# async def get_birth_date(
#     message: Message,
#     button: Button,
#     dialog_manager: DialogManager
# ):

#     # Получаем текст сообщения
#     text = message.text

#     # Проверяем, содержит ли текст дату в формате дд.мм.гггг
#     if re.match(r'\d{2}\.\d{2}\.\d{4}', text):
#         # Переформатируем дату в формат гггг-мм-дд
#         date_obj = datetime.strptime(text, '%d.%m.%Y')
#         formatted_date = date_obj.strftime('%Y-%m-%d')

#         # Проверяем корректность возраста
#         today = datetime.now()
#         age = today.year - date_obj.year - \
#             ((today.month, today.day) < (date_obj.month, date_obj.day))
#         if age >= 0 and age <= 150:
#             # Обновляем данные диалога
#             dialog_manager.dialog_data.update(birth_date=formatted_date)
#             # Переходим к следующему этапу или действию
#             await dialog_manager.switch_to(state=Survay.full_name, show_mode=ShowMode.SEND)
#         else:
#             await message.answer("Пожалуйста, введите реальный возраст.")


async def get_full_name(
    message: Message,
    button: Button,
    dialog_manager: DialogManager
):
    # Получаем текст сообщения
    text = message.text.title()

    # Проверяем, содержит ли текст ФИО (предполагаем, что ФИО состоит из букв, пробелов и может содержать дефисы)
    if re.match(r'^[a-zA-Zа-яА-ЯёЁ]+\s+[a-zA-Zа-яА-ЯёЁ]+\s+[a-zA-Zа-яА-ЯёЁ-]+$', text):
        # ФИО в верном формате, обновляем данные диалога
        dialog_manager.dialog_data.update(full_name=text)

        # Переходим к проверке поста
        await dialog_manager.switch_to(
            state=Survay.age, show_mode=ShowMode.SEND)


async def get_age(
    message: Message,
    button: Button,
    dialog_manager: DialogManager
):
    # Получаем текст сообщения
    text = message.text

    if re.match(r'^\d+$', text):

        age = int(text)
        if age > 0 and age < 120:
            # Возраст в верном формате, обновляем данные диалога
            dialog_manager.dialog_data.update(age=age)
            # Переходим к следующему этапу или действию
            await dialog_manager.switch_to(state=Survay.phone, show_mode=ShowMode.SEND)
        else:
            await message.reply("Пожалуйста, введите реальный возраст.")
    else:
        await message.reply("Пожалуйста, введите возраст цифрами.")


async def get_phone(
    message: Message,
    button: Button,
    dialog_manager: DialogManager
):
    # Получаем текст сообщения
    text = message.text

    # Проверяем, содержит ли текст номер телефона в правильном формате
    if re.match(r'^\+7\d{10}$', text):
        # Номер телефона в верном формате, обновляем данные диалога
        dialog_manager.dialog_data.update(phone=text)

        # Переходим к следующему этапу или действию
        await dialog_manager.switch_to(state=Survay.surgery, show_mode=ShowMode.SEND)


async def get_surgery_date(
    message: Message,
    button: Button,
    dialog_manager: DialogManager
):
    # Получаем текст сообщения
    text = message.text

    # Заказчик требовал чтобы был пользовательский ввод
    # Обновляем данные диалога
    dialog_manager.dialog_data.update(operation_date=text)
    # Переходим к следующему этапу или действию
    await dialog_manager.switch_to(state=Survay.question1, show_mode=ShowMode.SEND)


async def answer_quest1(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    # Инициализируем словарь для получения баллов
    dialog_manager.dialog_data.update(
        neurologist_point=0,
        cardiac_surgeon_point=0,
        cardiologist_point=0,
        surgeon_point=0,
        total_point=0
    )

    answer_text = dialog_manager.middleware_data.get(
        'i18n').get(f'{button.text.text}'.strip('{}').replace('_', '-'))

    # Извлекаем текущие значения из dialog_data
    data = dialog_manager.dialog_data
    neurologist_point = data.get('neurologist_point', 0)
    cardiac_surgeon_point = data.get('cardiac_surgeon_point', 0)
    cardiologist_point = data.get('cardiologist_point', 0)
    total_point = data.get('total_point', 0)

    # Определяем количество баллов за ответ
    if button.widget_id == 'a' or button.widget_id == 'b':
        neurologist_point += 1
        point = 1
    elif button.widget_id == 'c':
        cardiologist_point += 2
        point = 2
    elif button.widget_id == 'd':
        cardiac_surgeon_point += 3
        point = 3
    elif button.widget_id == 'e':
        point = 0

    # Формируем текст с добавлением количества баллов
    response_text = f"{answer_text}, {point}б."

    # Обновляем данные диалога
    dialog_manager.dialog_data.update(
        answer1=response_text,
        neurologist_point=neurologist_point,
        cardiac_surgeon_point=cardiac_surgeon_point,
        cardiologist_point=cardiologist_point,
        total_point=total_point
    )

    # Переходим к следующему этапу или действию
    await dialog_manager.switch_to(state=Survay.question2, show_mode=ShowMode.EDIT)


async def answer_quest2(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    # Получаем текст сообщения (текст кнопки)
    answer_text = dialog_manager.middleware_data.get(
        'i18n').get(f'{button.text.text}'.strip('{}').replace('_', '-'))

    # Извлекаем текущие значения из dialog_data
    data = dialog_manager.dialog_data
    surgeon_point = data.get('surgeon_point', 0)

    # Определяем количество баллов за ответ
    if button.widget_id == 'a' or button.widget_id == 'b':
        surgeon_point += 3
        point = 3
    elif button.widget_id == 'c':
        point = 0

    # Формируем текст с добавлением количества баллов
    response_text = f"{answer_text}, {point}б."

    # Обновляем данные диалога
    dialog_manager.dialog_data.update(
        answer2=response_text,
        surgeon_point=surgeon_point,
    )

    # Переходим к следующему этапу или действию
    await dialog_manager.switch_to(state=Survay.question3, show_mode=ShowMode.EDIT)


async def answer_quest3(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):

    # Получаем текст сообщения (текст кнопки)
    answer_text = dialog_manager.middleware_data.get(
        'i18n').get(f'{button.text.text}'.strip('{}').replace('_', '-'))

    # Извлекаем текущие значения из dialog_data
    data = dialog_manager.dialog_data
    cardiac_surgeon_point = data.get('cardiac_surgeon_point', 0)
    surgeon_point = data.get('surgeon_point', 0)

    # Определяем количество баллов за ответ
    if button.widget_id == 'a':
        surgeon_point += 3
        cardiac_surgeon_point += 3
        point = 3
    elif button.widget_id == 'b':
        point = 0

    # Формируем текст с добавлением количества баллов
    response_text = f"{answer_text}, {point}б."

    # Обновляем данные диалога
    dialog_manager.dialog_data.update(
        answer3=response_text,
        cardiac_surgeon_point=cardiac_surgeon_point,
        surgeon_point=surgeon_point,
    )

    # Переходим к следующему этапу или действию
    await dialog_manager.switch_to(state=Survay.question4, show_mode=ShowMode.EDIT)


async def answer_quest4(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    # Получаем текст сообщения (текст кнопки)
    answer_text = dialog_manager.middleware_data.get(
        'i18n').get(f'{button.text.text}'.strip('{}').replace('_', '-'))

    # Извлекаем текущие значения из dialog_data
    data = dialog_manager.dialog_data
    cardiac_surgeon_point = data.get('cardiac_surgeon_point', 0)

    # Определяем количество баллов за ответ
    if button.widget_id == 'a':
        cardiac_surgeon_point += 3
        point = 3
    elif button.widget_id == 'b':
        point = 0

    # Формируем текст с добавлением количества баллов
    response_text = f"{answer_text}, {point}б."

    # Обновляем данные диалога
    dialog_manager.dialog_data.update(
        answer4=response_text,
        cardiac_surgeon_point=cardiac_surgeon_point,
    )

    # Переходим к следующему этапу или действию
    await dialog_manager.switch_to(state=Survay.question5, show_mode=ShowMode.EDIT)


async def answer_quest5(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    # Получаем текст сообщения (текст кнопки)
    answer_text = dialog_manager.middleware_data.get(
        'i18n').get(f'{button.text.text}'.strip('{}').replace('_', '-'))

    # Извлекаем текущие значения из dialog_data
    data = dialog_manager.dialog_data
    cardiac_surgeon_point = data.get('cardiac_surgeon_point', 0)

    # Определяем количество баллов за ответ
    if button.widget_id in ['a', 'b', 'c']:
        cardiac_surgeon_point += 3
        point = 3
    elif button.widget_id == 'd':
        point = 0

    # Формируем текст с добавлением количества баллов
    response_text = f"{answer_text}, {point}б."

    # Обновляем данные диалога
    dialog_manager.dialog_data.update(
        answer5=response_text,
        cardiac_surgeon_point=cardiac_surgeon_point,
    )

    # Переходим к следующему этапу или действию
    await dialog_manager.switch_to(state=Survay.question6, show_mode=ShowMode.EDIT)


async def answer_quest6(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    # Получаем текст сообщения (текст кнопки)
    answer_text = dialog_manager.middleware_data.get(
        'i18n').get(f'{button.text.text}'.strip('{}').replace('_', '-'))

    # Извлекаем текущие значения из dialog_data
    data = dialog_manager.dialog_data
    cardiac_surgeon_point = data.get('cardiac_surgeon_point', 0)

    # Определяем количество баллов за ответ
    if button.widget_id in ['a', 'b', 'c']:
        cardiac_surgeon_point += 3
        point = 3
    elif button.widget_id == 'd':
        point = 0

    # Формируем текст с добавлением количества баллов
    response_text = f"{answer_text}, {point}б."

    # Обновляем данные диалога
    dialog_manager.dialog_data.update(
        answer6=response_text,
        cardiac_surgeon_point=cardiac_surgeon_point,
    )

    # Переходим к следующему этапу или действию
    await dialog_manager.switch_to(state=Survay.question7, show_mode=ShowMode.EDIT)


async def answer_quest7(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    answer_text = dialog_manager.middleware_data.get(
        'i18n').get(f'{button.text.text}'.strip('{}').replace('_', '-'))

    points_mapping = {
        'a': 1,
        'b': 0,
    }

    point = points_mapping.get(button.widget_id, 0)
    response_text = f"{answer_text}, {point}б."

    dialog_manager.dialog_data.update(answer7=response_text)

    if button.widget_id == 'a':
        await dialog_manager.switch_to(state=Survay.question8, show_mode=ShowMode.EDIT)
    elif button.widget_id == 'b':
        await dialog_manager.switch_to(state=Survay.question10, show_mode=ShowMode.EDIT)


async def answer_quest8(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    answer_text = dialog_manager.middleware_data.get(
        'i18n').get(f'{button.text.text}'.strip('{}').replace('_', '-'))

    points_mapping = {
        'a': 0,
        'b': 1,
        'c': 3,
        'd': 0,
    }

    point = points_mapping.get(button.widget_id, 0)
    response_text = f"{answer_text}, {point}б."

    dialog_manager.dialog_data.update(answer8=response_text)

    await dialog_manager.switch_to(state=Survay.question9, show_mode=ShowMode.EDIT)


async def answer_quest9(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    answer_text = dialog_manager.middleware_data.get(
        'i18n').get(f'{button.text.text}'.strip('{}').replace('_', '-'))

    points_mapping = {
        'a': 0,
        'b': 1,
        'c': 3,
        'd': 0,
    }

    point = points_mapping.get(button.widget_id, 0)
    response_text = f"{answer_text}, {point}б."

    dialog_manager.dialog_data.update(answer9=response_text)

    await dialog_manager.switch_to(state=Survay.question10, show_mode=ShowMode.EDIT)


async def answer_quest10(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    answer_text = dialog_manager.middleware_data.get(
        'i18n').get(f'{button.text.text}'.strip('{}').replace('_', '-'))

    points_mapping = {
        'a': 3,
        'b': 0,
    }

    point = points_mapping.get(button.widget_id, 0)
    response_text = f"{answer_text}, {point}б."

    dialog_manager.dialog_data.update(answer10=response_text)
    if button.widget_id == 'a':
        dialog_manager.dialog_data.update(hobl='yes')

    await dialog_manager.switch_to(state=Survay.question11, show_mode=ShowMode.EDIT)


async def answer_quest11(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
):
    answer_text = dialog_manager.middleware_data.get(
        'i18n').get(f'{button.text.text}'.strip('{}').replace('_', '-'))

    points_mapping = {
        'a': 3,
        'b': 0,
    }

    point = points_mapping.get(button.widget_id, 0)
    response_text = f"{answer_text}, {point}б."
    hobl = dialog_manager.dialog_data.get('hobl')
    dialog_manager.dialog_data.update(answer11=response_text)
    if button.widget_id == 'a':
        dialog_manager.dialog_data.update(somke='yes')
        await dialog_manager.switch_to(state=Survay.question12, show_mode=ShowMode.EDIT)
    elif hobl:
        await dialog_manager.switch_to(state=Survay.question13, show_mode=ShowMode.EDIT)
    else:
        await dialog_manager.switch_to(state=Survay.imt_height, show_mode=ShowMode.EDIT)


async def answer_quest12(
        message: Message,
        button: Button,
        dialog_manager: DialogManager
):
    text = message.text
    text = text.replace(',', '')
    if re.match(r'^\d+(\.\d+)?$', text):

        сigarettes = float(text)
        dialog_manager.dialog_data.update(answer12=сigarettes)
        await dialog_manager.switch_to(state=Survay.question13, show_mode=ShowMode.SEND)
    else:
        await message.reply("Пожалуйста, введите количество цифрами.")


async def answer_quest13(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    answer_text = dialog_manager.middleware_data.get(
        'i18n').get(f'{button.text.text}'.strip('{}').replace('_', '-'))

    points_mapping = {
        'a': 3,
        'b': 0,
    }

    point = points_mapping.get(button.widget_id, 0)
    response_text = f"{answer_text}, {point}б."

    dialog_manager.dialog_data.update(answer13=response_text)

    await dialog_manager.switch_to(state=Survay.question14, show_mode=ShowMode.EDIT)


async def answer_quest14(
        allback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    answer_text = dialog_manager.middleware_data.get(
        'i18n').get(f'{button.text.text}'.strip('{}').replace('_', '-'))

    points_mapping = {
        'a': 3,
        'b': 0,
    }

    point = points_mapping.get(button.widget_id, 0)
    response_text = f"{answer_text}, {point}б."

    dialog_manager.dialog_data.update(answer14=response_text)

    await dialog_manager.switch_to(state=Survay.imt_height, show_mode=ShowMode.EDIT)


async def answer_imt_height(
        message: Message,
        button: Button,
        dialog_manager: DialogManager
):
    text = message.text.strip()

    # Удаляем запятые и пробелы из ввода
    text = text.replace(',', '')

    # Проверяем, что введено целое число
    if re.match(r'^\d+$', text):
        height_cm = int(text)
        # Проверяем, что рост находится в разумном диапазоне (50 см - 250 см)
        if 50 <= height_cm <= 250:
            # Конвертируем рост из см в метры (для последующего использования в расчетах)
            imt_height = height_cm / 100
            dialog_manager.dialog_data.update(imt_height=imt_height)
            await dialog_manager.switch_to(state=Survay.imt_weight, show_mode=ShowMode.SEND)
        else:
            await message.reply("Пожалуйста, введите рост в диапазоне от 50 до 250 сантиметров.")
    else:
        await message.reply("Пожалуйста, введите корректное целое число в сантиметрах.")


async def answer_imt_weight(
        message: Message,
        button: Button,
        dialog_manager: DialogManager
):
    text = message.text.strip()
    text = text.replace(',', '.')
    if re.match(r'^\d+(\.\d+)?$', text):
        imt_weight = float(text)
        # Проверяем, что масса находится в разумном диапазоне (20 кг - 500 кг)
        if 20 <= imt_weight <= 500:
            imt_height = dialog_manager.dialog_data.get('imt_height')

            imt = imt_weight / imt_height
            dialog_manager.dialog_data.update(imt=round(imt, 2))
            await dialog_manager.switch_to(state=Survay.wash, show_mode=ShowMode.EDIT)

        else:
            await message.reply("Пожалуйста, введите массу в кг в диапазоне от 20 до 500 кг.")
    else:
        await message.reply("Пожалуйста, введите корректное число в килограммах.")


async def answer_pain_scale(
        message: Message,
        button: Button,
        dialog_manager: DialogManager
):
    # Получаем ответ пользователя в виде текста
    text = message.text.strip()

    # Проверяем, что введено корректное число от 1 до 6
    if text.isdigit() and 1 <= int(text) <= 6:
        # Словарь для соответствия чисел и баллов
        number_to_score = {
            '1': 'Боль отсутствует (0 б.)',
            '2': 'Слабая боль (1-3 б.)',
            '3': 'Умеренная боль (4 б.)',
            '4': 'Сильная боль (6 б.)',
            '5': 'Очень сильная боль (7-9 б.)',
            '6': 'Нестерпиммая боль (10 б.)',
        }

        pain_score = number_to_score[text]
        dialog_manager.dialog_data.update(pain_scale=pain_score)
        # Здесь можно сохранить pain_score в базу данных или выполнять другие действия с результатом
        await dialog_manager.switch_to(state=Survay.self_assessment, show_mode=ShowMode.SEND)
    else:
        await message.reply("Пожалуйста, введите число от 1 до 6 для ответа.")


async def answer_assessment(
        message: Message,
        button: Button,
        dialog_manager: DialogManager
):
    text = message.text.strip()

    text = text.replace(',', '.')
    # Проверяем, что введено число или десятичная дробь
    if re.match(r'^\d+(\.\d+)?$', text):
        self_assessment = float(text)
        if 0.0 <= self_assessment <= 100.0:

            dialog_manager.dialog_data.update(
                self_assessment=self_assessment,
                user_id=message.from_user.id
            )

            # Получаем текст сообщения (текст кнопки)
            answer_text = dialog_manager.middleware_data.get(
                'i18n').get('normal-result')

            session = dialog_manager.middleware_data.get('session')

            data = dialog_manager.dialog_data
            # Вставляем данные в базу данных
            await orm_add_info_surv(session, data)

            response_text = await generate_response(data, answer_text)
            dialog_manager.dialog_data.update(response_text=response_text)
            await dialog_manager.switch_to(state=Survay.survay_result, show_mode=ShowMode.SEND)

        else:
            await message.reply("Пожалуйста, введите значение в диапазоне от 0 до 100.")
    else:
        await message.reply("Пожалуйста, введите корректное число.")
