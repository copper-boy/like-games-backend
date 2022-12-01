from pydantic import BaseModel

from structures.enums import CardPositionEnum


class CardSchema(BaseModel):
    id: int

    rank: str
    suit: str

    position: CardPositionEnum
    to_id: int

    class Config:
        orm_mode = True
