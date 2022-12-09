from pydantic import BaseModel

from structures.enums import RoundTypeEnum


class RoundSchema(BaseModel):
    id: int

    type: RoundTypeEnum

    class Config:
        orm_mode = True
