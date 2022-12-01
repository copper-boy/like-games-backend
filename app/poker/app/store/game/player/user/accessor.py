from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from orm import UserModel
from store.base import BaseAccessor


class UserAccessor(BaseAccessor):
    async def create_user(self, session: AsyncSession, user_id: int) -> UserModel:
        to_return = UserModel(user_id=user_id)

        session.add(to_return)

        return to_return

    async def is_have_player(self, session: AsyncSession, user_id: int) -> bool:
        cursor = await session.execute(
            select(UserModel).where(UserModel.id == user_id).options(joinedload(UserModel.player))
        )
        to_check = cursor.scalar()

        return bool(to_check.player)

    async def get_user_by(self, session: AsyncSession, where: Any) -> UserModel:
        to_return = await session.execute(select(UserModel).where(where))

        return to_return.scalar()
