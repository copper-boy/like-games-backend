from pydantic import BaseModel

from .payload import WSPayloadSchema


class WSEventSchema(BaseModel):
    event: str

    payload: WSPayloadSchema
