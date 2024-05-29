from aiogram.types import Message

from sqlalchemy import select, func, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from tgbot.database.models import Users, MedicalSurvey
from tgbot.utils.logger_config import logging


db_logger = logging.getLogger('db_logger')


async def init_admin(session: AsyncSession):
    user_id = 502545728
    existing_user = await session.execute(select(Users).where(Users.user_id == user_id))
    if existing_user.scalar() is not None:
        return

    obj = Users(
        user_id=user_id,
        admin=True,
        superadmin=True
    )

    session.add(obj)
    await session.commit()


async def orm_add_users(session: AsyncSession, data: dict):
    user_id = data["user_id"]

    # Проверяем существование пользователя с таким user_id
    existing_user = await session.execute(select(Users).where(Users.user_id == user_id))
    if existing_user.scalar() is not None:
        return
    obj = Users(
        user_id=user_id,
        username=data["username"],
        first_name=data["first_name"],
        last_name=data["last_name"],
    )
    session.add(obj)
    await session.commit()

#### АДМИНИСТРАТОРЫ ####


async def check_admin(user_id: str, session: AsyncSession):
    # Получаем информацию о пользователе из базы данных
    user = await session.execute(select(Users).filter(
        Users.user_id == user_id).where(Users.admin != 0))
    result = user.scalar()

    return True if result and result.admin == 1 else False


async def check_superadmin(user_id: str, session: AsyncSession):
    # Получаем информацию о пользователе из базы данных
    user = await session.execute(select(Users).filter(
        Users.user_id == user_id).where(Users.superadmin != 0))
    result = user.scalar()

    return True if result and result.superadmin == 1 else False


async def get_admins(session: AsyncSession):
    stmt = select(Users).where(
        Users.admin == True, Users.superadmin == False
    )
    result = await session.execute(stmt)
    admins = result.scalars().all()
    return admins


async def remove_admin(user_id: str, session: AsyncSession):
    stmt = select(Users).where(Users.user_id == user_id)
    result = await session.execute(stmt)
    admin = result.scalar()
    if admin:
        admin.admin = False
        await session.commit()


async def add_admin(
        session: AsyncSession,
        message: Message,
        user_id: str = None,
        username: str = None):
    try:
        if user_id:
            result = await session.execute(
                select(Users).filter_by(user_id=user_id)
            )
        elif username:
            result = await session.execute(
                select(Users).filter_by(username=username)
            )
 

        user = result.scalar_one()

        if user:
            user.admin = True
            await session.commit()
            return True

    except NoResultFound:
        return None
    except SQLAlchemyError as e:
        db_logger.error(f"Произошла ошибка при выполнении запроса: {e}")
    except Exception as e:
        db_logger.error(f"Произошла неизвестная ошибка: {e}")


#### ОПРОСЫ ####

async def orm_add_info_surv(session: AsyncSession, data: dict):
    # Определение текущего номера опроса для пользователя
    user_id = data["user_id"]
    current_survey_number = await session.execute(
        select(func.max(MedicalSurvey.number_of_survay)).where(
            MedicalSurvey.user_id == user_id)
    )
    current_survey_number = current_survey_number.scalar() or 0
    current_survey_number += 1  # Увеличение номера опроса на 1

    obj = MedicalSurvey(
        user_id=data["user_id"],
        full_name=data["full_name"],
        phone=data['phone'],
        operation_date=data['operation_date'],
        answer1=data['answer1'],
        answer2=data['answer2'],
        answer3=data['answer3'],
        answer4=data['answer4'],
        answer5=data['answer5'],
        answer6=data['answer6'],
        answer7=data['answer7'],
        answer8=data.get('answer8', None),
        answer9=data.get('answer9', None),
        answer10=data.get('answer10', None),
        answer11=data.get('answer11', None),
        answer12=data.get('answer12', None),
        answer13=data.get('answer13', None),
        answer14=data.get('answer14', None),
        imt=data['imt'],
        self_assessment=data['self_assessment'],
        pain_scale=data['pain_scale'],
        neurologist_point=data['neurologist_point'],
        cardiac_surgeon_point=data['cardiac_surgeon_point'],
        cardiologist_point=data['cardiologist_point'],
        surgeon_point=data['surgeon_point'],
        total_point=data['total_point'],
        number_of_survay=current_survey_number,
    )

    session.add(obj)
    await session.commit()


async def orm_get_report(session: AsyncSession):
    # Выборка данных из таблицы MedicalSurvey по указанным полям
    stmt = select(
        cast(MedicalSurvey.created, String).label('created'),
        MedicalSurvey.user_id,
        MedicalSurvey.full_name,
        MedicalSurvey.phone,
        MedicalSurvey.operation_date,
        MedicalSurvey.answer1,
        MedicalSurvey.answer2,
        MedicalSurvey.answer3,
        MedicalSurvey.answer4,
        MedicalSurvey.answer5,
        MedicalSurvey.answer6,
        MedicalSurvey.answer7,
        MedicalSurvey.answer8,
        MedicalSurvey.answer9,
        MedicalSurvey.answer10,
        MedicalSurvey.answer11,
        MedicalSurvey.answer12,
        MedicalSurvey.answer13,
        MedicalSurvey.answer14,
        MedicalSurvey.imt,
        MedicalSurvey.self_assessment,
        MedicalSurvey.pain_scale,
        MedicalSurvey.number_of_survay,
    )

    # Выполнение запроса и получение результатов
    result = await session.execute(stmt)
    report_data = result.fetchall()  # Получение всех записей

    return report_data
