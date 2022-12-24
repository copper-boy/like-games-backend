from pydantic import BaseConfig, BaseModel


class PotServiceSchema(BaseModel):
    class Config(BaseConfig):
        orm_mode = True
