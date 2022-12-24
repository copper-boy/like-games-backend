from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from orm import UserModel
from store.base import BaseAccessor


class UserAccessor(BaseAccessor):
    async def create_user(self, session: AsyncSession, user_id: int) -> UserModel:  # noqa
        to_return = UserModel(user_id=user_id)

        session.add(to_return)

        return to_return

    async def is_have_player(self, session: AsyncSession, user_id: int) -> bool:
        user = await self.get_user_by(session=session, where=(UserModel.id == user_id))

        return bool(user.player)

    async def get_user_by(self, session: AsyncSession, where: Any) -> UserModel:  # noqa
        to_return = await session.execute(
            select(UserModel).where(where).options(joinedload(UserModel.player))
        )

        return to_return.scalar()
