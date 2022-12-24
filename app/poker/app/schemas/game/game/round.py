from __future__ import annotations

from structures.enums import RoundTypeEnum

from ...base import PokerServiceSchema


class RoundSchema(PokerServiceSchema):
    id: int

    type: RoundTypeEnum
