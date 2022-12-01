from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, Enum, Integer, String

from db.base import Base
from structures.enums import RegistrationTypeEnum


class UserModel(Base):
    id = Column(Integer, primary_key=True, index=True)
    telegram = Column(BigInteger, default=None, nullable=True)

    email = Column(String, unique=True, index=True, nullable=True)
    username = Column(String)
    password = Column(String, nullable=True)

    registration_type = Column(Enum(RegistrationTypeEnum), default=RegistrationTypeEnum.provided)
    join = Column(DateTime, default=datetime.utcnow)
