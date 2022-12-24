from __future__ import annotations

from typing import Optional

from pydantic import EmailStr

from structures.enums import RegistrationTypeEnum

from .base import UserServiceSchema


class UserRegistrationSchema(UserServiceSchema):
    email: EmailStr
    username: str
    password: str


class UserTelegramRegistrationSchema(UserServiceSchema):
    telegram: int
    username: str


class UserLoginSchema(UserServiceSchema):
    email: EmailStr
    password: str


class UserSchema(UserServiceSchema):
    id: int
    telegram: Optional[int] = None
    email: Optional[EmailStr] = None
    username: str
    registration_type: RegistrationTypeEnum


class UserViewSchema(UserServiceSchema):
    id: int
    telegram: Optional[int] = None
    username: str
