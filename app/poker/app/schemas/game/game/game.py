from pydantic import BaseModel


class GameSchema(BaseModel):
    id: int

    min_players: int
    max_players: int

    chips_to_join: int

    small_blind: int
    big_blind: int

    class Config:
        orm_mode = True
