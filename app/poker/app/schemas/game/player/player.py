from pydantic import BaseModel

from .user import UserSchema


class PlayerSchema(BaseModel):
    id: int

    game_chips: int

    in_game_order: int

    last_bet: int
    round_bet: int

    is_allin: bool
    is_folded: bool

    user: UserSchema

    class Config:
        orm_mode = True
