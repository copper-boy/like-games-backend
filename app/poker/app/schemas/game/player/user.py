from __future__ import annotations

from ...base import PokerServiceSchema


class UserSchema(PokerServiceSchema):
    id: int

    user_id: int

    class Config:
        orm_mode = True
