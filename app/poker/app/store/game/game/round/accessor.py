from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from orm import RoundModel

from structures import enums, exceptions
from store.base import BaseAccessor


class RoundAccessor(BaseAccessor):
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

    async def call_next_round(
        self, session: AsyncSession, round_id: int
    ) -> RoundModel:
        round = await self.get_round_by(session=session, where=(RoundModel.id == round_id))

        if not round.round_ended:
            raise exceptions.DatabaseAccessorError

        match round.type:
            case enums.RoundTypeEnum.preflop:
                to_update = enums.RoundTypeEnum.flop
            case enums.RoundTypeEnum.flop:
                to_update = enums.RoundTypeEnum.river
            case enums.RoundTypeEnum.river:
                to_update = enums.RoundTypeEnum.turn
            case enums.RoundTypeEnum.turn:
                to_update = enums.RoundTypeEnum.showdown
            case enums.RoundTypeEnum.showdown:
                to_update = enums.RoundTypeEnum.preflop
            case _:
                raise exceptions.DatabaseAccessorError

        await self.update_round(session=session, round_id=round.id, type=to_update)
