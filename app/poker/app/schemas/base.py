from pydantic import BaseConfig, BaseModel


class PokerServiceSchema(BaseModel):
    class Config(BaseConfig):
        orm_mode = True
