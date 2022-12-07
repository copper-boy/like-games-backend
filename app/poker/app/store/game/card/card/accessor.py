from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from orm import CardModel, DeckModel
from schemas.game import LogicCardSchema
from store.base import BaseAccessor
from structures.enums import CardPositionEnum


class CardAccessor(BaseAccessor):
    async def create_card(
        self, session: AsyncSession, deck: DeckModel, card: LogicCardSchema
    ) -> CardModel:
        to_return = CardModel(rank=card.rank, suit=card.suit, deck=deck)

        session.add(to_return)

        return to_return

    async def update_card(
        self,
        session: AsyncSession,
        card_id: int,
        position: CardPositionEnum,
        to_id: int,
    ) -> None:
        await session.execute(
            update(CardModel).where(CardModel.id == card_id).values(position=position, to_id=to_id)
        )

    async def set_new(self, session: AsyncSession, card_id: int, card: LogicCardSchema) -> None:
        to_dict = card.dict()
        await session.execute(update(CardModel).where(CardModel.id == card_id).values(**to_dict))

    async def get_cards_by(self, session: AsyncSession, where: Any) -> list[CardModel]:
        to_return = await session.execute(select(CardModel).where(where))

        return to_return.scalars().all()
