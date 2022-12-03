from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from orm import RoundModel
from store.base import BaseAccessor
from structures import enums, exceptions


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

    async def create_round(self, session: AsyncSession) -> RoundModel:
        to_return = RoundModel()

        session.add(to_return)

        return to_return

    async def is_already_taken(self, session: AsyncSession, round_id: int) -> bool:
        cursor = await session.execute(
            select(RoundModel)
            .where(RoundModel.id == round_id)
            .options(joinedload(RoundModel.session))
        )
        to_check = cursor.scalar()

        return bool(
            to_check.session
        )  # If no relationship is assigned to RoundModel.session then bool cast will return False.

    async def update_round(self, session: AsyncSession, round_id: int, **kwargs: dict) -> None:
        await session.execute(update(RoundModel).where(RoundModel.id == round_id).values(**kwargs))

    async def get_round_by(self, session: AsyncSession, where: Any) -> RoundModel:
        to_return = await session.execute(select(RoundModel).where(where))

        return to_return.scalar()

    async def call_next_round(self, session: AsyncSession, round_id: int) -> RoundModel:
        round = await self.get_round_by(session=session, where=(RoundModel.id == round_id))
        if not round.round_ended:
            raise exceptions.DatabaseAccessorError

        to_update = self.to_select.get(round.type, None)
        await self.update_round(session=session, round_id=round.id, type=to_update)
