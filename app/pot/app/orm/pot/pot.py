from sqlalchemy import BigInteger, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.base import Base


class PotModel(Base):
    id = Column(Integer, primary_key=True)

    pot = Column(BigInteger, default=15000)

    user_id = Column(Integer, ForeignKey("usermodel.id"))
    user = relationship("UserModel", back_populates="pot")
