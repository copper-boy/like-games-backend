from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from orm import GameModel
from store.base import BaseAccessor


class GameAccessor(BaseAccessor):
    async def create_game(  # noqa
        self,
        session: AsyncSession,
        min_players: int = 2,
        max_players: int = 9,
        chips_to_join: int = 10000,
        small_blind: int = 50,
        big_blind: int = 100,
    ) -> GameModel:
        to_return = GameModel(
            min_players=min_players,
            max_players=max_players,
            chips_to_join=chips_to_join,
            small_blind=small_blind,
            big_blind=big_blind,
        )

        session.add(to_return)

        return to_return

    async def get_game_by(self, session: AsyncSession, where: Any) -> GameModel:  # noqa
        to_return = await session.execute(select(GameModel).where(where))

        return to_return.scalar()
