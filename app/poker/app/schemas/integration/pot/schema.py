from pydantic import BaseModel


class PotSchema(BaseModel):
    id: int | None = None
    user_id: int | None = None
    pot: int | None = None


class PotUpdateSchema(BaseModel):
    pot: int
