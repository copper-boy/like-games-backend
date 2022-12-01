from sqlalchemy import Column, Enum, Integer
from sqlalchemy.orm import relationship

from db.base import Base
from structures.enums import GameTypeEnum


class GameModel(Base):
    id = Column(Integer, primary_key=True)

    type = Column(Enum(GameTypeEnum), default=GameTypeEnum.texas)

    min_players = Column(Integer, default=2)
    max_players = Column(Integer, default=9)

    chips_to_join = Column(Integer, default=10000)

    small_blind = Column(Integer, default=50)
    big_blind = Column(Integer, default=100)

    sessions = relationship("SessionModel", back_populates="game")
