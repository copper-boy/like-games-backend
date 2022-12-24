from __future__ import annotations

from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from core.tools import store
from orm import UserModel

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify password with hashed password.

    :param: password: not encrypted password
    :param: hashed_password: encrypted password
    :return: True if hash and password did match else False
    """
    try:
        return pwd_context.verify(password, hashed_password)
    except (ValueError, TypeError):
        return False


def get_password_hash(password: str) -> str:
    """
    Returns the encrypted password based on the normal password.

    :param: password: not encrypted password
    :return: hashed password
    """
    return pwd_context.hash(password)


async def authenticate_user(
    session: AsyncSession, email: EmailStr, password: str
) -> UserModel | None:
    user = await store.user_accessor.get_user_by(session=session, where=(UserModel.email == email))
    if not user or not verify_password(password=password, hashed_password=user.password):
        return None

    return user
