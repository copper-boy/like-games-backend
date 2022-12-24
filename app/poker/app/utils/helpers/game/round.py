from __future__ import annotations

from typing import Optional

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from core import tools
from db.session import session as sessionmaker
from orm import CardModel, PlayerModel, SessionModel
from schemas import IntegrationLikeEvaluatorRequestSchema
from structures.enums import CardPositionEnum, RoundTypeEnum
from utils import helpers


async def __set_next_round(
    asyncsession: AsyncSession,
    session: SessionModel,
    expression: Optional[bool],
    to_id: int,
) -> None:
    if not to_id:
        return None

    if expression:
        player = await helpers.get_player_by_id(session=asyncsession, player_id=to_id)
        if player.round_bet == session.max_bet or player.is_allin:
            await tools.store.game_player_accessor.clear_players(
                session=asyncsession, session_id=session.id
            )

            await tools.store.game_round_accessor.call_next_round(
                session=asyncsession, round_id=session.round_id
            )


async def __preflop(asyncsession: AsyncSession, session: SessionModel) -> None:
    players = await tools.store.game_player_accessor.get_players_by(
        session=asyncsession, where=(PlayerModel.session_id == session.id)
    )
    for player in players:
        await helpers.give_player_cards(
            session=asyncsession,
            deck_id=session.deck_id,
            player_id=player.id,
        )
    await helpers.give_table_cards(
        session=asyncsession, deck_id=session.deck_id, round_type=session.round.type
    )

    await __set_next_round(
        asyncsession=asyncsession,
        session=session,
        expression=(
            session.last_player == session.big_blind_position
            and session.current_player == session.small_blind_position
        ),
        to_id=session.big_blind_position,
    )


async def __any_flop_to_river(asyncsession: AsyncSession, session: SessionModel) -> None:
    if await helpers.is_all_allin(session=asyncsession, session_id=session.id):
        expression = True
    else:
        expression = session.last_player == session.small_blind_position

    await __set_next_round(
        asyncsession=asyncsession,
        session=session,
        expression=expression,
        to_id=session.small_blind_position,
    )


async def __showdown(asyncsession: AsyncSession, session: SessionModel) -> None:
    board = await tools.store.card_accessor.get_cards_by(
        session=asyncsession,
        where=and_(
            CardModel.position == CardPositionEnum.table,
            CardModel.deck_id == session.deck_id,
        ),
    )
    board_list = [f"{card.rank}{card.suit}" for card in board]

    players = await tools.store.game_player_accessor.get_players_by(
        session=asyncsession, where=(PlayerModel.session_id == session.id)
    )

    hands: dict[int, str] = {}
    for index, player in enumerate(players, start=0):
        hand = await tools.store.card_accessor.get_cards_by(
            session=asyncsession,
            where=and_(
                CardModel.position == CardPositionEnum.player,
                CardModel.to_id == PlayerModel.id,
                CardModel.deck_id == session.deck_id,
            ),
        )
        hands[index] = "".join(f"{card.rank}{card.suit}" for card in hand)
    hands_list = list(hands.values())

    print(
        await tools.store.integration_like_accessor.find_winners(
            json=IntegrationLikeEvaluatorRequestSchema(board=board_list, hands=hands_list)
        )
    )


async def _next_round_call(
    asyncsession: AsyncSession,
    session_id: int,
) -> RoundTypeEnum:
    session = await helpers.get_session_with_raise(session=asyncsession, session_id=session_id)
    to_call = {RoundTypeEnum.preflop: __preflop, RoundTypeEnum.showdown: __showdown}
    await to_call.get(session.round.type, __any_flop_to_river)(
        asyncsession=asyncsession, session=session
    )

    return session.round.type


async def next_round_call(
    session_id: int,
    asyncsession: Optional[AsyncSession] = None,
) -> RoundTypeEnum:
    if asyncsession:
        result = await _next_round_call(asyncsession=asyncsession, session_id=session_id)
    else:
        async with sessionmaker.begin() as asyncsession:
            result = await _next_round_call(asyncsession=asyncsession, session_id=session_id)

    return result
