from pydantic import BaseModel

from structures.enums import RoundTypeEnum


class RoundSchema(BaseModel):
    id: int

    type: RoundTypeEnum

    round_ended: bool
    rounds_played: int

    all_played: bool

    class Config:
        orm_mode = True
