from __future__ import annotations

from typing import Any

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from orm import UserModel
from store.base import BaseAccessor


class UserAccessor(BaseAccessor):
    async def create_user(self, session: AsyncSession, user_id: int) -> UserModel:  # noqa
        to_return = await session.execute(
            insert(UserModel).values(user_id=user_id).returning(UserModel)
        )

        return to_return.one()

    async def get_user_by(self, session: AsyncSession, where: Any) -> UserModel:  # noqa
        to_return = await session.execute(
            select(UserModel).where(where).options(joinedload(UserModel.player))
        )

        return to_return.scalar()
