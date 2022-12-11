from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.base import Base


class PlayerModel(Base):
    id = Column(Integer, primary_key=True)

    game_chips = Column(Integer, default=10000)

    last_bet = Column(Integer, default=0)
    round_bet = Column(Integer, default=0)

    is_allin = Column(Boolean, default=False)
    is_folded = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("usermodel.id"), unique=True)
    user = relationship("UserModel", back_populates="player", uselist=False)

    session_id = Column(Integer, ForeignKey("sessionmodel.id"))
    session = relationship("SessionModel", back_populates="players")
