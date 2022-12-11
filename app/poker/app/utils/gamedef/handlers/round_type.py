from asyncio import create_task

from sqlalchemy.ext.asyncio import AsyncSession

from utils import helpers


async def round_type(
    session: AsyncSession,
    current_player: int,
    max_bet: int,
    manager,
) -> None:
    player = await helpers.get_player_by_id(session=session, player_id=current_player)
    connection = manager.connection(user_id=player.user_id)

    if player.round_bet == max_bet or player.is_allin:
        if connection.timeout_task:
            connection.timeout_task.cancel()
            connection.timeout_task = None
    else:
        if not connection.timeout_task:
            connection.timeout_task = create_task(
                helpers.wait_for_action(
                    manager=manager,
                    player_id=player.id,
                    user_id=player.user,
                )
            )
