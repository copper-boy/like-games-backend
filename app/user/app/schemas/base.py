from pydantic import BaseConfig, BaseModel


class UserServiceSchema(BaseModel):
    class Config(BaseConfig):
        orm_mode = True
