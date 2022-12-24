from __future__ import annotations

from typing import Any

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from orm import RoundModel
from store.base import BaseAccessor
from structures import enums


class RoundAccessor(BaseAccessor):
    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        super(RoundAccessor, self).__init__(*args, **kwargs)

        self.to_select = {
            enums.RoundTypeEnum.preflop: enums.RoundTypeEnum.flop,
            enums.RoundTypeEnum.flop: enums.RoundTypeEnum.river,
            enums.RoundTypeEnum.river: enums.RoundTypeEnum.turn,
            enums.RoundTypeEnum.turn: enums.RoundTypeEnum.showdown,
            enums.RoundTypeEnum.showdown: enums.RoundTypeEnum.preflop,
        }

    async def create_round(self, session: AsyncSession) -> RoundModel:  # noqa
        to_return = await session.execute(insert(RoundModel).returning(RoundModel))

        return to_return.one()

    async def update_round(  # noqa
        self, session: AsyncSession, round_id: int, values: dict
    ) -> None:  # noqa
        await session.execute(update(RoundModel).where(RoundModel.id == round_id).values(**values))

    async def get_round_by(self, session: AsyncSession, where: Any) -> RoundModel:  # noqa
        to_return = await session.execute(
            select(RoundModel).where(where).options(joinedload(RoundModel.session))
        )

        return to_return.scalar()

    async def call_next_round(self, session: AsyncSession, round_id: int) -> enums.RoundTypeEnum:
        round = await self.get_round_by(session=session, where=(RoundModel.id == round_id))  # noqa

        to_update = self.to_select.get(round.type, None)
        await self.update_round(session=session, round_id=round.id, values={"type": to_update})

        return to_update
