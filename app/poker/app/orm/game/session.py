from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.base import Base
from structures.enums import PlayerActionEnum


class SessionModel(Base):
    id = Column(Integer, primary_key=True)

    deck_id = Column(Integer, ForeignKey("deckmodel.id"))
    deck = relationship("DeckModel", back_populates="session")

    game_id = Column(Integer, ForeignKey("gamemodel.id"))
    game = relationship("GameModel", back_populates="sessions")

    players = relationship("PlayerModel", back_populates="session")

    small_blind_position = Column(Integer, default=0)
    big_blind_position = Column(Integer, default=0)

    current_player = Column(Integer, default=0)

    last_player = Column(Integer, default=0)
    last_player_action = Column(Enum(PlayerActionEnum), default=PlayerActionEnum.unknown)

    in_progress = Column(Boolean, default=False)

    max_bet = Column(Integer, default=0)

    pot = Column(Integer, default=0)

    round_id = Column(Integer, ForeignKey("roundmodel.id"))
    round = relationship("RoundModel", back_populates="session")
