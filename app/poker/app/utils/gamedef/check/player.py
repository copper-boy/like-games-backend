from sqlalchemy.ext.asyncio import AsyncSession

from core import tools
from utils import helpers
from ws import WSManager


async def check_player(
    session: AsyncSession,
    manager: WSManager,
    session_id: int,
    player_id: int,
) -> None:
    player = await helpers.get_player_by_id(session=session, player_id=player_id)

    if player.game_chips == 0 and not player.is_allin:
        await helpers.delete_player(manager=manager, player_id=player_id)

    if player.is_allin or player.is_folded:
        await tools.store.game_session_accessor.set_next_player(
            session=session, session_id=session_id
        )
