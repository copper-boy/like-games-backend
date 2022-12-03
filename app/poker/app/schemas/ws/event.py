from pydantic import BaseModel


class WSEventSchema(BaseModel):
    command: str
    payload: dict | None = None
