from pydantic import BaseModel, EmailStr

from structures.enums import RegistrationTypeEnum


class UserSchema(BaseModel):
    id: int
    telegram: int | None
    email: EmailStr | None
    username: str
    registration_type: RegistrationTypeEnum
