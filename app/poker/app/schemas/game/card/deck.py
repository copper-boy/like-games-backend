from pydantic import BaseModel

from .card import CardSchema


class DeckSchema(BaseModel):
    id: int

    cards: list[CardSchema]

    class Config:
        orm_mode = True
