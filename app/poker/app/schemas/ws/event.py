from __future__ import annotations

from typing import Optional

from likeevents.schema import LikeEventSchema
from structures.enums import EventEnum

from .payload import PayloadSchema


class EventSchema(LikeEventSchema):
    path: str
    payload: Optional[PayloadSchema] = None

    @property
    def type(self) -> EventEnum:
        type: list[str] = []  # noqa

        for letter in self.path:
            if letter.isupper():
                break
            type.append(letter)

        return EventEnum("like_" + "".join(type))
