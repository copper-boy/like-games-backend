from __future__ import annotations

from loguru import logger

from core import tools
from utils import gamedef


async def _gamedef_thread(session_id: int) -> None:
    try:
        manager = tools.ws_managers.get(session_id=session_id)
    except KeyError as e:
        logger.exception(e)
        return None

    await gamedef.gamedef(manager=manager, session_id=session_id)


async def gamedef_thread(session_id: int) -> None:
    await _gamedef_thread(session_id=session_id)
