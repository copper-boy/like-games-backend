from asyncio import create_task

from sqlalchemy.ext.asyncio import AsyncSession

from utils import helpers


async def any_flop_to_river(session: AsyncSession, manager, session_id: int) -> None:
    s = await helpers.get_session_with_raise(session=session, session_id=session_id)

    if not (s.last_player == s.big_blind_position and s.current_player == s.small_blind_position):
        player = await helpers.get_player_by_id(session=session, player_id=s.current_player)
        connection = manager.connection(user_id=player.user_id)

        if player.last_bet == s.max_bet or player.game_chips == 0:
            if connection.timeout_task:
                connection.timeout_task.cancel()
        else:
            if not connection.timeout_task:
                connection.timeout_task = create_task(
                    helpers.wait_for_action(
                        manager=manager,
                        player_id=player.id,
                        user_id=player.user,
                    )
                )
