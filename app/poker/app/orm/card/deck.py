from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from db.base import Base


class DeckModel(Base):
    id = Column(Integer, primary_key=True)

    cards = relationship("CardModel", back_populates="deck")
