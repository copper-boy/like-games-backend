from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from orm import PlayerModel, SessionModel, UserModel
from store.base import BaseAccessor
from structures.exceptions import DatabaseAccessorError


class PlayerAccessor(BaseAccessor):
    async def create_player(
        self, session: AsyncSession, user: UserModel, assign_to: SessionModel
    ) -> PlayerModel:
        is_have_player = await self.store.game_user_accessor.is_have_player(
            session=session, user_id=user.id
        )
        if is_have_player:
            raise DatabaseAccessorError

        to_return = PlayerModel(user=user, session=assign_to)

        session.add(to_return)

        return to_return

    async def delete_player(self, session: AsyncSession, player_id: int) -> None:
        await session.execute(delete(PlayerModel).where(PlayerModel.id == player_id))

    async def get_player_by(self, session: AsyncSession, where: Any) -> PlayerModel:
        to_return = await session.execute(
            select(PlayerModel).where(where).options(joinedload(PlayerModel.user))
        )

        return to_return.scalar()
