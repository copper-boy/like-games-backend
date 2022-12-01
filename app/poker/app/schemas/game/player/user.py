from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int

    user_id: int

    class Config:
        orm_mode = True
