from pydantic import BaseModel
from pydantic.class_validators import validator

from structures.constants import CARD_RANK, CARD_SUIT


class CardSchema(BaseModel):
    rank: str
    suit: str

    @validator("rank")
    def rank_validator(cls, v: str) -> str:
        value = v.upper()
        if value not in CARD_RANK:
            raise ValueError("not allowed rank")

        return value

    @validator("suit")
    def suit_validator(cls, v: str) -> str:
        value = v.lower()
        if value not in CARD_SUIT:
            raise ValueError("not allowed suit")

        return value
