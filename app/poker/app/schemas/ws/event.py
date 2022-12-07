from pydantic import BaseModel

from structures.enums import WSEventEnum

from .payload import WSPayloadSchema


class WSEventSchema(BaseModel):
    event: WSEventEnum

    payload: WSPayloadSchema
