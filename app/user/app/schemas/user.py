from pydantic import BaseModel, EmailStr

from structures.enums import RegistrationTypeEnum


class UserRegistrationSchema(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserTelegramRegistrationSchema(BaseModel):
    telegram: int
    username: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    id: int
    telegram: int | None
    email: EmailStr | None
    username: str
    registration_type: RegistrationTypeEnum

    class Config:
        orm_mode = True


class UserViewSchema(BaseModel):
    id: int
    telegram: int | None
    username: str

    class Config:
        orm_mode = True
