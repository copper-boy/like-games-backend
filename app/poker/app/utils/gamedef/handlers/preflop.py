from asyncio import create_task

from sqlalchemy.ext.asyncio import AsyncSession

from core import tools
from utils import helpers
from ws import WSManager


async def preflop(session: AsyncSession, manager: WSManager, session_id: int) -> None:
    s = await helpers.get_session_with_raise(session=session, session_id=session_id)

    if s.last_player == s.small_blind_position and s.current_player == s.big_blind_position:
        big_blind_player = await helpers.get_player_by_id(
            session=session, player_id=s.big_blind_position
        )
        connection = manager.connection(user_id=big_blind_player.user_id)

        if big_blind_player.last_bet == s.max_bet or big_blind_player.game_chips == 0:
            if connection.timeout_task:
                connection.timeout_task.close()

            await tools.store.game_round_accessor.update_round(
                session=session,
                round_id=s.round_id,
                values={
                    "round_ended": True,
                },
            )
            await tools.store.game_round_accessor.call_next_round(
                session=session, round_id=s.round_id
            )
            await helpers.set_blinds(session=s, session_id=s.id)
        else:
            connection.timeout_task = create_task(
                helpers.wait_for_action(
                    manager=manager,
                    player_id=big_blind_player.id,
                    user_id=big_blind_player.user,
                )
            )
    else:
        player = await helpers.get_player_by_id(session=session, player_id=s.current_player)
        connection = manager.connection(user_id=player.user_id)

        if player.last_bet == s.max_bet or player.game_chips == 0:
            if connection.timeout_task:
                connection.timeout_task.close()
        else:
            connection.timeout_task = create_task(
                helpers.wait_for_action(
                    manager=manager,
                    player_id=player.id,
                    user_id=player.user,
                )
            )
