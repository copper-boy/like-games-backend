from __future__ import annotations

from .base import PotServiceSchema


class PotSchema(PotServiceSchema):
    id: int
    user_id: int
    pot: int

    class Config:
        orm_mode = True


class PotUpdateSchema(PotServiceSchema):
    pot: int
