from __future__ import annotations

from typing import Any

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from orm import CardModel
from schemas.game import LogicCardSchema
from store.base import BaseAccessor
from structures.enums import CardPositionEnum


class CardAccessor(BaseAccessor):
    async def create_card(  # noqa
        self, session: AsyncSession, deck_id: int, card: LogicCardSchema
    ) -> CardModel:
        to_return = await session.execute(
            insert(CardModel)
            .values(rank=card.rank, suit=card.suit, deck_id=deck_id)
            .returning(CardModel)
        )

        return to_return

    async def update_card(  # noqa
        self,
        session: AsyncSession,
        card_id: int,
        position: CardPositionEnum,
        to_id: int,
    ) -> None:
        await session.execute(
            update(CardModel).where(CardModel.id == card_id).values(position=position, to_id=to_id)
        )

    async def set_new(
        self, session: AsyncSession, card_id: int, card: LogicCardSchema
    ) -> None:  # noqa
        to_dict = card.dict()
        await session.execute(update(CardModel).where(CardModel.id == card_id).values(**to_dict))

    async def get_cards_by(self, session: AsyncSession, where: Any) -> list[CardModel]:  # noqa
        to_return = await session.execute(select(CardModel).where(where))

        return to_return.scalars().all()
