from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from orm import DeckModel
from store.base import BaseAccessor
from structures.enums import CardPositionEnum
from structures.exceptions.game.errors import NotAcceptablePositionError


class DeckAccessor(BaseAccessor):
    async def create_deck(self, session: AsyncSession) -> DeckModel:
        to_return = DeckModel()

        cards_to_insert = self.store.logic_deck_accessor.make_deck(with_shuffle=True)

        for card_to_insert in cards_to_insert.deck:
            await self.store.card_accessor.create_card(
                session=session, deck=to_return, card=card_to_insert
            )

        session.add(to_return)

        return to_return

    async def get_deck_by(self, session: AsyncSession, where: Any) -> DeckModel:
        to_return = await session.execute(
            select(DeckModel).where(where).options(joinedload(DeckModel.cards))
        )

        return to_return.scalar()

    async def give_max_cards(
        self,
        session: AsyncSession,
        deck_id: int,
        position: CardPositionEnum,
        to_id: int,
    ) -> None:
        deck = await self.get_deck_by(session=session, where=(DeckModel.id == deck_id))

        match position:
            case CardPositionEnum.player:
                to_access, max_value = 0, 2
            case CardPositionEnum.table:
                to_access, max_value = 0, 5
            case _:
                raise NotAcceptablePositionError

        for card in deck.cards:
            if card.to_id != 0 and card.position != CardPositionEnum.deck:
                continue
            if to_access == max_value:
                break
            await self.store.card_accessor.update_card(
                session=session, card_id=card.id, position=position, to_id=to_id
            )
            to_access += 1

    async def delete_deck(self, session: AsyncSession, deck_id: int) -> None:
        await session.execute(delete(DeckModel).where(DeckModel.id == deck_id))
