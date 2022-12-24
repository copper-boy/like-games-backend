from __future__ import annotations

from ...base import PokerServiceSchema
from .user import UserSchema


class PlayerSchema(PokerServiceSchema):
    id: int

    game_chips: int

    last_bet: int
    round_bet: int

    is_allin: bool
    is_folded: bool

    user: UserSchema
