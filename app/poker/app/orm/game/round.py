from sqlalchemy import Boolean, Column, Enum, Integer
from sqlalchemy.orm import relationship

from db.base import Base
from structures.enums import RoundTypeEnum


class RoundModel(Base):
    id = Column(Integer, primary_key=True)

    type = Column(Enum(RoundTypeEnum), default=RoundTypeEnum.preflop)

    session = relationship("SessionModel", back_populates="round", uselist=False)
