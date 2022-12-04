from pydantic import BaseModel


class CommandPayloadSchema(BaseModel):
    with_descriptions: bool = False
