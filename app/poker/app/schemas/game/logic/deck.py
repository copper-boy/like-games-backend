from pydantic import BaseModel

from .card import CardSchema


class DeckSchema(BaseModel):
    deck: list[CardSchema]
