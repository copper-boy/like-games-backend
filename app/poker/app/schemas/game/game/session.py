from pydantic import BaseModel

from structures.enums import PlayerActionEnum


class SessionSchema(BaseModel):
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

    class Config:
        orm_mode = True


class SessionFilterCountSchema(BaseModel):
    count: int

    class Config:
        orm_mode = True
