from aiogram import html
from aiogram.types import User
from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from tgbot.database.orm_query import check_admin, check_superadmin


# async def username_getter(event_from_user: User, **kwargs):
#     is_admin = await check_admin(event_from_user.id)
#     return {'username': event_from_user.username,
#             'is_admin': is_admin}


async def is_superadmin(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    session = dialog_manager.middleware_data.get('session')
    is_super = await check_superadmin(event_from_user.id, session)
    return {'is_super': is_super}


async def text_assesment(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "assessment": i18n.get('assessment'),
        'instruction_button': i18n.get('instruction-button'),
    }


async def text_instruction(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "assessment_button": i18n.get('assessment-button'),
        "instruction": i18n.get('instruction')
    }


async def pre_survay(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "birth_day": i18n.get('birth-date-input'),
        "full_name": i18n.get('full-name-input'),
        "age": i18n.get('age-input'),
        "phone": i18n.get('phone-input'),
        "surgery": i18n.get('surgery-input'),
    }


async def username_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    **kwargs,
) -> dict[str, str]:
    session = dialog_manager.middleware_data.get('session')
    is_admin = await check_admin(event_from_user.id, session)
    return {'username': event_from_user.username,
            'is_admin': is_admin,
            "hello_user":  i18n.get('start-message'),
            'rate_btn': i18n.get('start-rate-button'),
            "url_button": i18n.get('url-button')
            }


async def survay_question1(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "question1": i18n.get('question1'),
        "quest1_btn1": i18n.get('quest1-btn1'),
        "quest1_btn2": i18n.get('quest1-btn2'),
        "quest1_btn3": i18n.get('quest1-btn3'),
        "quest1_btn4": i18n.get('quest1-btn4'),
        "quest1_btn5": i18n.get('quest1-btn5'),
    }


async def survay_question2(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "question2": i18n.get('question2'),
        "quest2_btn1": i18n.get('quest2-btn1'),
        "quest2_btn2": i18n.get('quest2-btn2'),
        "quest2_btn3": i18n.get('quest2-btn3'),
    }


async def survay_question3(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "question3": i18n.get('question3'),
        "btn_yes": i18n.get('btn-yes'),
        "btn_no": i18n.get('btn-no'),
    }


async def survay_question4(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "question4": i18n.get('question4'),
        "btn_yes": i18n.get('btn-yes'),
        "btn_no": i18n.get('btn-no'),
    }


async def survay_question5(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "question5": i18n.get('question5'),
        "quest5_btn1": i18n.get('quest5-btn1'),
        "quest5_btn2": i18n.get('quest5-btn2'),
        "quest5_btn3": i18n.get('quest5-btn3'),
        "btn_no": i18n.get('btn-no'),
    }


async def survay_question6(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "question6": i18n.get('question6'),
        "quest6_btn1": i18n.get('quest6-btn1'),
        "quest6_btn2": i18n.get('quest6-btn2'),
        "quest6_btn3": i18n.get('quest6-btn3'),
        "quest6_btn4": i18n.get('quest6-btn4'),
    }


async def survay_question7(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "question7": i18n.get('question7'),
        "btn_yes": i18n.get('btn-yes'),
        "btn_no": i18n.get('btn-no'),
    }


async def survay_question8(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "question8": i18n.get('question8'),
        "quest8_btn1": i18n.get('quest8-btn1'),
        "quest8_btn2": i18n.get('quest8-btn2'),
        "quest8_btn3": i18n.get('quest8-btn3'),
        "quest8_btn4": i18n.get('quest8-btn4'),
    }


async def survay_question9(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "question9": i18n.get('question9'),
        "quest9_btn1": i18n.get('quest9-btn1'),
        "quest9_btn2": i18n.get('quest9-btn2'),
        "quest9_btn3": i18n.get('quest9-btn3'),
        "quest9_btn4": i18n.get('quest9-btn4'),
    }


async def survay_question10(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "question10": i18n.get('question10'),
        "btn_yes": i18n.get('btn-yes'),
        "btn_no": i18n.get('btn-no'),
    }


async def survay_question11(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "question11": i18n.get('question11'),
        "btn_yes": i18n.get('btn-yes'),
        "btn_no": i18n.get('btn-no'),
    }


async def survay_question12(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "question12": i18n.get('question12'),
    }


async def survay_question13(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "question13": i18n.get('question13'),
        "btn_yes": i18n.get('btn-yes'),
        "btn_no": i18n.get('btn-no'),
    }


async def survay_question14(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "question14": i18n.get('question14'),
        "btn_yes": i18n.get('btn-yes'),
        "btn_no": i18n.get('btn-no'),
    }


async def imt(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "imt_height": i18n.get('imt-height'),
        "imt_weight": i18n.get('imt-weight'),
    }


async def wash(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "wash": i18n.get('wash'),
    }


async def self_assessment(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    return {
        "self_assessment": i18n.get('self-assessment'),
    }


async def get_result(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> dict[str, str]:
    response_text = dialog_manager.dialog_data.get('response_text')
    return {
        "url_button": i18n.get('url-button'),
        "response_text": response_text,
    }
