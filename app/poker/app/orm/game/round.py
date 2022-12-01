from sqlalchemy import Boolean, Column, Enum, Integer
from sqlalchemy.orm import relationship

from db.base import Base
from structures.enums import RoundTypeEnum


class RoundModel(Base):
    id = Column(Integer, primary_key=True)

    type = Column(Enum(RoundTypeEnum), default=RoundTypeEnum.preflop)

    round_ended = Column(Boolean, default=False)
    rounds_played = Column(Integer, default=0)

    all_played = Column(Boolean, default=False)

    session = relationship("SessionModel", back_populates="round", uselist=False)
