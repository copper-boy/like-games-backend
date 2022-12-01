from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from db.base import Base


class UserModel(Base):
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, unique=True, nullable=False)

    player = relationship("PlayerModel", back_populates="user", uselist=False)
