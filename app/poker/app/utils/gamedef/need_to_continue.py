from db.session import session as sessionmaker
from orm import SessionModel
from structures.enums import RoundTypeEnum
from utils import gamedef, helpers

from .check import check_player


def _generate_preflop_answer(session: SessionModel) -> dict:
    return {
        "last_player": session.last_player,
        "current_player": session.current_player,
        "from_position": session.small_blind_position,
        "to_position": session.big_blind_position,
        "max_bet": session.max_bet,
    }


async def need_to_continue(manager, session_id: int) -> None:
    to_call = {RoundTypeEnum.preflop: _generate_preflop_answer}

    async with sessionmaker.begin() as asyncsession:
        session = await helpers.get_session_with_raise(session=asyncsession, session_id=session_id)
        async with asyncsession.begin_nested() as nested_asyncsession:
            await check_player(
                session=nested_asyncsession.session,
                manager=manager,
                session_id=session.id,
                player_id=session.current_player,
            )
        kwargs = to_call[session.round.type](session)
        await gamedef.handlers.round_type(session=asyncsession, manager=manager, **kwargs)
