from __future__ import annotations

from ...base import PokerServiceSchema
from .card import CardSchema


class DeckSchema(PokerServiceSchema):
    id: int

    cards: list[CardSchema]
