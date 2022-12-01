from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import tools
from orm import UserModel
from utils import token


async def get_user(
    authorize: AuthJWT,
    session: AsyncSession,
) -> UserModel:
    current_user = token.get_jwt_subject(authorize=authorize)

    user = await tools.store.user_accessor.get_user_by(
        session=session, where=(UserModel.id == current_user)
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found on server"
        )

    return user


async def get_user_by_raw_token(
    authorize: AuthJWT,
    raw_token: str,
    session: AsyncSession,
) -> UserModel:
    current_user = token.get_raw_jwt_subject(authorize=authorize, raw_token=raw_token)

    user = await tools.store.user_accessor.get_user_by(
        session=session, where=(UserModel.id == current_user)
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found on server"
        )

    return user
