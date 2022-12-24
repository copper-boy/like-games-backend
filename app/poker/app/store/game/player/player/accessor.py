from __future__ import annotations

from typing import Any

from sqlalchemy import asc, delete, func, select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from orm import PlayerModel, SessionModel, UserModel
from store.base import BaseAccessor
from structures.exceptions import DatabaseAccessorError


class PlayerAccessor(BaseAccessor):
    async def create_player(
        self, session: AsyncSession, game_chips: int, user: UserModel, assign_to: SessionModel
    ) -> PlayerModel:
        if user:
            is_have_player = await self.store.game_user_accessor.is_have_player(
                session=session, user_id=user.id
            )
            if is_have_player:
                raise DatabaseAccessorError

        to_return = PlayerModel(game_chips=game_chips, user=user, session=assign_to)

        session.add(to_return)

        return to_return

    async def update_player(  # noqa
        self, session: AsyncSession, player_id: int, values: dict
    ) -> None:  # noqa
        await session.execute(
            update(PlayerModel).where(PlayerModel.id == player_id).values(**values)
        )

    async def delete_player(self, session: AsyncSession, player_id: int) -> None:  # noqa
        await session.execute(delete(PlayerModel).where(PlayerModel.id == player_id))

    async def __get_cursor(self, session: AsyncSession, where: Any) -> CursorResult:  # noqa
        to_return = await session.execute(
            select(PlayerModel)
            .where(where)
            .options(joinedload(PlayerModel.user))
            .options(joinedload(PlayerModel.session))
        )

        return to_return

    async def get_player_by(self, session: AsyncSession, where: Any) -> PlayerModel:
        to_return = await self.__get_cursor(session=session, where=where)

        return to_return.scalar()

    async def get_players_by(self, session: AsyncSession, where: Any) -> list[PlayerModel]:
        to_return = await self.__get_cursor(session=session, where=where)

        return to_return.scalars().all()

    async def get_players_count(self, session: AsyncSession, session_id: int) -> int:  # noqa
        to_return = await session.execute(
            select(func.count(PlayerModel.id))
            .where(PlayerModel.session_id == session_id)
            .select_from(PlayerModel)
        )

        return to_return.scalar()

    async def get_players_by_order_in_game_order(  # noqa
        self,
        session: AsyncSession,
        session_id: int,
    ) -> list[PlayerModel]:
        to_return = await session.execute(
            select(PlayerModel)
            .where(PlayerModel.session_id == session_id)
            .order_by(asc(PlayerModel.id))
        )

        return to_return.scalars().all()

    async def clear_players(self, session: AsyncSession, session_id: int) -> None:  # noqa
        await session.execute(
            update(PlayerModel)
            .where(PlayerModel.session_id == session_id)
            .values(last_bet=0, round_bet=0)
        )
