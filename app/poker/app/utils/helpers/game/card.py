from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from core import tools
from structures.enums import CardPositionEnum, RoundTypeEnum


async def clear_deck(session: AsyncSession, deck_id: int, deck_length: int = 52) -> None:
    await tools.store.deck_accessor.give_cards(
        session=session,
        deck_id=deck_id,
        position=CardPositionEnum.deck,
        to_id=0,
        count=deck_length,
    )


async def give_player_cards(
    session: AsyncSession, deck_id: int, player_id: int, player_hand_length: int = 2
) -> None:
    await tools.store.deck_accessor.give_cards(
        session=session,
        deck_id=deck_id,
        position=CardPositionEnum.player,
        to_id=player_id,
        count=player_hand_length,
    )


_to_add = {
    RoundTypeEnum.preflop: 0,
    RoundTypeEnum.flop: 3,
    RoundTypeEnum.turn: 1,
    RoundTypeEnum.river: 1,
}


async def give_table_cards(session: AsyncSession, deck_id: int, round_type: RoundTypeEnum) -> None:
    count = _to_add[round_type]

    await tools.store.deck_accessor.give_cards(
        session=session, deck_id=deck_id, position=CardPositionEnum.table, to_id=0, count=count
    )


async def shuffle_deck(session: AsyncSession, deck_id: int) -> None:
    await tools.store.deck_accessor.shuffle_deck(session=session, deck_id=deck_id)
