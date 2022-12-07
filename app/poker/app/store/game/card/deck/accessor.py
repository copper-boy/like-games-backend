from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from orm import CardModel, DeckModel
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

    async def is_already_taken(self, session: AsyncSession, deck_id: int) -> bool:
        deck = await self.get_deck_by(session=session, where=(DeckModel.id == deck_id))

        return bool(deck.session)

    async def get_deck_by(self, session: AsyncSession, where: Any) -> DeckModel:
        to_return = await session.execute(
            select(DeckModel)
            .where(where)
            .options(joinedload(DeckModel.cards))
            .options(joinedload(DeckModel.session))
        )

        return to_return.scalar()

    async def shuffle_deck(self, session: AsyncSession, deck_id: int) -> None:
        deck = await self.get_deck_by(session=session, where=(DeckModel.id == deck_id))
        cards_to_shuffle = self.store.logic_deck_accessor.make_deck(with_shuffle=True)

        for index, card in enumerate(cards_to_shuffle.deck, start=0):
            card_id = deck.cards[index].id
            await self.store.card_accessor.set_new(session=session, card_id=card_id, card=card)

    async def give_cards(
        self,
        session: AsyncSession,
        deck_id: int,
        position: CardPositionEnum,
        to_id: int,
        count: int,
    ) -> None:
        deck = await self.get_deck_by(session=session, where=(DeckModel.id == deck_id))

        to_access = 0
        for card in deck.cards:
            if card.to_id != 0 and card.position != CardPositionEnum.deck:
                continue
            if to_access == count:
                break
            await self.store.card_accessor.update_card(
                session=session, card_id=card.id, position=position, to_id=to_id
            )
            to_access += 1

    async def delete_deck(self, session: AsyncSession, deck_id: int) -> None:
        await session.execute(delete(DeckModel).where(DeckModel.id == deck_id))
