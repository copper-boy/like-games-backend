from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from core import tools
from db.session import session as sessionmaker
from orm import SessionModel
from structures.enums import RoundTypeEnum
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


async def _next_round_call(
    asyncsession: AsyncSession,
    session_id: int,
) -> RoundTypeEnum:
    session = await helpers.get_session_with_raise(session=asyncsession, session_id=session_id)

    match session.round.type:
        case RoundTypeEnum.preflop:

            await __set_next_round(
                asyncsession=asyncsession,
                session=session,
                expression=(
                    session.last_player == session.big_blind_position
                    and session.current_player == session.small_blind_position
                ),
                to_id=session.big_blind_position,
            )
        case RoundTypeEnum.showdown:
            # TODO: find winner here
            ...
        case _:
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

    return session.round.type


async def next_round_call(
    session_id: int,
    manager,
    asyncsession: Optional[AsyncSession] = None,
) -> RoundTypeEnum:
    if asyncsession:
        result = await _next_round_call(
            asyncsession=asyncsession, session_id=session_id, manager=manager
        )
    else:
        async with sessionmaker.begin() as asyncsession:
            result = await _next_round_call(
                asyncsession=asyncsession, session_id=session_id, manager=manager
            )

    return result
