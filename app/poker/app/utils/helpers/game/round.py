from sqlalchemy.ext.asyncio import AsyncSession

from core import tools
from db.session import session as sessionmaker
from orm import SessionModel
from structures.enums import RoundTypeEnum
from utils import helpers


async def _preflop(
    asyncsession: AsyncSession,
    session: SessionModel,
    manager,
) -> None:
    if (
        session.last_player == session.small_blind_position
        and session.current_player == session.big_blind_position
    ):
        print("okay")

        big_blind_player = await helpers.get_player_by_id(
            session=asyncsession, player_id=session.big_blind_position
        )
        connection = manager.connection(user_id=big_blind_player.user_id)

        print(big_blind_player.round_bet)

        if big_blind_player.round_bet == session.max_bet or big_blind_player.is_allin:
            if connection.timeout_task:
                connection.timeout_task.cancel()

            await tools.store.game_player_accessor.clear_players(
                session=asyncsession, session_id=session.id
            )

            await tools.store.game_round_accessor.call_next_round(
                session=asyncsession, round_id=session.round_id
            )

            await helpers.set_blinds(session=asyncsession, session_id=session.id)


async def _default(
    asyncsession: AsyncSession,
    session: SessionModel,
    manager,
) -> None:
    ...


async def next_round_call(session_id: int, manager) -> RoundTypeEnum:
    to_call = {RoundTypeEnum.preflop: _preflop}

    async with sessionmaker.begin() as asyncsession:
        session = await helpers.get_session_with_raise(session=asyncsession, session_id=session_id)

        await to_call.get(session.round.type, _default)(
            asyncsession=asyncsession, session=session, manager=manager
        )

    return session.round.type
