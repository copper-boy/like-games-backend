from __future__ import annotations

from pydantic import BaseModel


class PotSchema(BaseModel):
    id: int
    user_id: int
    pot: int


class PotUpdateSchema(BaseModel):
    pot: int
