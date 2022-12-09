from asyncio import create_task

from sqlalchemy.ext.asyncio import AsyncSession

from utils import helpers


async def round_type(
    session: AsyncSession,
    last_player: int,
    current_player: int,
    from_position: int,
    to_position: int,
    max_bet: int,
    manager,
) -> None:
    if not (last_player == from_position and current_player == to_position):
        player = await helpers.get_player_by_id(session=session, player_id=current_player)
        connection = manager.connection(user_id=player.user_id)

        if player.last_bet == max_bet or player.is_allin:
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
