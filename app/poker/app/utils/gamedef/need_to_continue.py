from core import tools
from db.session import session as sessionmaker
from orm import SessionModel
from structures.enums import RoundTypeEnum
from utils import gamedef
from ws import WSManager

from .check import check_player


async def need_to_continue(manager: WSManager, session_id: int) -> None:
    to_call = {
        RoundTypeEnum.preflop: gamedef.handlers.preflop,
        RoundTypeEnum.flop: gamedef.handlers.any_flop_to_river,
        RoundTypeEnum.turn: gamedef.handlers.any_flop_to_river,
        RoundTypeEnum.river: gamedef.handlers.any_flop_to_river,
    }

    async with sessionmaker.begin() as asyncsession:
        session = await tools.store.game_session_accessor.get_session_by(
            session=asyncsession, where=(SessionModel.id == session_id)
        )
        async with asyncsession.begin_nested() as nested_asyncsession:
            await check_player(
                session=nested_asyncsession.session,
                manager=manager,
                session_id=session.id,
                player_id=session.current_player,
            )

        await to_call[session.round.type](
            session=asyncsession, manager=manager, session_id=session.id
        )
