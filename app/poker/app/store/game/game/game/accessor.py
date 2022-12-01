from typing import Any

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from orm import GameModel
from store.base import BaseAccessor
from structures.enums import GameTypeEnum


class GameAccessor(BaseAccessor):
    async def create_game(
        self,
        session: AsyncSession,
        type: GameTypeEnum = GameTypeEnum.texas,
        min_players: int = 2,
        max_players: int = 9,
        chips_to_join: int = 10000,
        small_blind: int = 50,
        big_blind: int = 100,
    ) -> GameModel:
        to_return = GameModel(
            type=type,
            min_players=min_players,
            max_players=max_players,
            chips_to_join=chips_to_join,
            small_blind=small_blind,
            big_blind=big_blind,
        )

        session.add(to_return)

        return to_return

    async def get_game_by(self, session: AsyncSession, where: Any) -> GameModel:
        to_return = await session.execute(select(GameModel).where(where))

        return to_return.scalar()
