from __future__ import annotations

from structures.enums import PlayerActionEnum

from ...base import PokerServiceSchema


class SessionSchema(PokerServiceSchema):
    id: int

    game_id: int

    small_blind_position: int
    big_blind_position: int

    current_player: int

    last_player: int
    last_player_action: PlayerActionEnum

    in_progress: bool

    round_id: int

    max_bet: int

    pot: int


class SessionFilterCountSchema(PokerServiceSchema):
    count: int
