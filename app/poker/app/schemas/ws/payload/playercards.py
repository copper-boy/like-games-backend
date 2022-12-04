from pydantic import BaseModel


class PlayercardsPayloadSchema(BaseModel):
    player_id: int
