from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.base import Base
from structures.enums import PlayerActionEnum


class SessionModel(Base):
    id = Column(Integer, primary_key=True)

    game_id = Column(Integer, ForeignKey("gamemodel.id"))
    game = relationship("GameModel", back_populates="sessions")

    players = relationship("PlayerModel", back_populates="session")
    players_connected = Column(Integer, default=0)

    dealer_position = Column(Integer, default=0)
    small_blind_position = Column(Integer, default=0)
    big_blind_position = Column(Integer, default=0)

    current_player = Column(Integer, default=0)

    last_player = Column(Integer, default=0)
    last_player_action = Column(Enum(PlayerActionEnum), default=PlayerActionEnum.unknown)

    in_progress = Column(Boolean, default=False)

    round_id = Column(Integer, ForeignKey("roundmodel.id"))
    round = relationship("RoundModel", back_populates="session")
