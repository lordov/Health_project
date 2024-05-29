from sqlalchemy import Integer, String,  DateTime,  Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(
        DateTime(), default=datetime.now())
    updated: Mapped[DateTime] = mapped_column(
        DateTime(), default=datetime.now(), onupdate=datetime.now())


class Users(Base):
    __tablename__ = 'bot_users'

    user_id: Mapped[str] = mapped_column(String(150), primary_key=True)
    username: Mapped[str] = mapped_column(String(150), nullable=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    admin: Mapped[bool] = mapped_column(default=False)
    superadmin: Mapped[bool] = mapped_column(default=False)


class MedicalSurvey(Base):
    __tablename__ = 'medical_survey'

    survey_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(150),
                                         ForeignKey('bot_users.user_id'), nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=True)
    phone: Mapped[str] = mapped_column(String(150), nullable=True)
    operation_date: Mapped[str] = mapped_column(String(150), nullable=True)
    answer1: Mapped[str] = mapped_column(String(150), nullable=True)
    answer2: Mapped[str] = mapped_column(String(150), nullable=True)
    answer3: Mapped[str] = mapped_column(String(150), nullable=True)
    answer4: Mapped[str] = mapped_column(String(150), nullable=True)
    answer5: Mapped[str] = mapped_column(String(150), nullable=True)
    answer6: Mapped[str] = mapped_column(String(150), nullable=True)
    answer7: Mapped[str] = mapped_column(String(150), nullable=True)
    answer8: Mapped[str] = mapped_column(String(150), nullable=True)
    answer9: Mapped[str] = mapped_column(String(150), nullable=True)
    answer10: Mapped[str] = mapped_column(String(150), nullable=True)
    answer11: Mapped[str] = mapped_column(String(150), nullable=True)
    answer12: Mapped[str] = mapped_column(String(150), nullable=True)
    answer13: Mapped[str] = mapped_column(String(150), nullable=True)
    answer14: Mapped[str] = mapped_column(String(150), nullable=True)
    imt: Mapped[float] = mapped_column(Float, nullable=True)
    self_assessment: Mapped[Float] = mapped_column(Float, nullable=True)
    pain_scale: Mapped[str] = mapped_column(String(150), nullable=True)
    neurologist_point: Mapped[int] = mapped_column(Integer, nullable=True)
    cardiac_surgeon_point: Mapped[int] = mapped_column(Integer, nullable=True)
    cardiologist_point: Mapped[int] = mapped_column(Integer, nullable=True)
    surgeon_point: Mapped[int] = mapped_column(Integer, nullable=True)
    total_point: Mapped[int] = mapped_column(Integer, nullable=True)
    number_of_survay: Mapped[int] = mapped_column(Integer, nullable=False)
    user = relationship("Users", backref="medical_surveys")
