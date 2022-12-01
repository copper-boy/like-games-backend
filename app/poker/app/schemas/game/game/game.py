from pydantic import BaseModel

from structures.enums import GameTypeEnum


class GameSchema(BaseModel):
    id: int

    type: GameTypeEnum

    min_players: int
    max_players: int

    chips_to_join: int

    small_blind: int
    big_blind: int

    class Config:
        orm_mode = True
