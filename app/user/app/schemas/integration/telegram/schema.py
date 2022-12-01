from pydantic import BaseModel


class TelegramOAuth2ResponseSchema(BaseModel):
    id: int
    username: str
