from __future__ import annotations

from structures.enums import CardPositionEnum

from ...base import PokerServiceSchema


class CardSchema(PokerServiceSchema):
    id: int

    rank: str
    suit: str

    position: CardPositionEnum
    to_id: int
