from pydantic import BaseModel

from structures.enums import PlayerActionEnum

from .game import GameSchema
from .round import RoundSchema


class SessionSchema(BaseModel):
    id: int

    game_id: int
    game: GameSchema

    dealer_position: int
    small_blind_position: int
    big_blind_position: int

    current_player: int

    last_player: int
    last_player_action: PlayerActionEnum

    in_progress: bool

    round_id: int
    round: RoundSchema

    class Config:
        orm_mode = True


class SessionFilterCountSchema(BaseModel):
    count: int

    class Config:
        orm_mode = True
