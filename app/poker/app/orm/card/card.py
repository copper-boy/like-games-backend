from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base
from structures.enums import CardPositionEnum


class CardModel(Base):
    id = Column(Integer, primary_key=True)

    rank = Column(String)
    suit = Column(String)

    position = Column(Enum(CardPositionEnum), default=CardPositionEnum.deck)
    to_id = Column(Integer, default=0)

    deck_id = Column(Integer, ForeignKey("deckmodel.id"))
    deck = relationship("DeckModel", back_populates="cards")
