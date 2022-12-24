from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, EmailStr

from structures.enums import RegistrationTypeEnum


class UserSchema(BaseModel):
    id: int
    telegram: Optional[int] = None
    email: Optional[EmailStr] = None
    username: str
    registration_type: RegistrationTypeEnum
