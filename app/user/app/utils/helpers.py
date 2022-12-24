from __future__ import annotations

import token

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.ext.asyncio import AsyncSession

from core import tools
from orm import UserModel


async def optional_user(authorize: AuthJWT, session: AsyncSession) -> UserModel | None:
    try:
        authorize.jwt_required()

        subject = token.get_jwt_subject(authorize=authorize)

        optional = await tools.store.user_accessor.get_user_by(
            session=session, where=(UserModel.id == subject)
        )
    except AuthJWTException:
        optional = None

    return optional


async def create_new_user(
    session: AsyncSession,
    hashed_password: str,
    email: str,
    username: str,
) -> UserModel:
    async with session.begin_nested() as nested_session:
        user = await tools.store.user_accessor.create_user(
            session=nested_session.session,
            email=email,
            username=username,
            password=hashed_password,
        )

    return user


async def create_new_user_telegram(
    session: AsyncSession, telegram: int, username: str
) -> UserModel:
    user = await tools.store.user_accessor.get_user_by(
        session=session, where=(UserModel.telegram == telegram)
    )
    if not user:
        async with session.begin_nested() as nested_session:
            user = await tools.store.user_accessor.create_user_telegram(
                session=nested_session.session,
                telegram=telegram,
                username=username,
            )

    return user


async def link_to_exists(session: AsyncSession, user_id: int, telegram: int) -> None:
    async with session.begin_nested() as nested_session:
        await tools.store.user_accessor.update_user(
            session=nested_session.session,
            user_id=user_id,
            telegram=telegram,
        )
