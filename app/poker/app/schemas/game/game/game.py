from __future__ import annotations

from ...base import PokerServiceSchema


class GameSchema(PokerServiceSchema):
    id: int

    min_players: int
    max_players: int

    chips_to_join: int

    small_blind: int
    big_blind: int
