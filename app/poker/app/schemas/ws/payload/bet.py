from pydantic import BaseModel


class BetPayloadSchema(BaseModel):
    bet: int
