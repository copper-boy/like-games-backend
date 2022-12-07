from asyncio import sleep

from schemas import WSEventSchema
from ws import WSManager


async def wait_for_action(manager: WSManager, player_id: int, user_id: int) -> None:
    await manager.broadcast_json(
        event=WSEventSchema(
            event="game", payload={"to_filter": "wait_for_action", "data": {"timeout": 10}}
        )
    )
    await sleep(10)

    await manager.broadcast_json(
        event=WSEventSchema(
            event="game",
            payload={
                "to_filter": "wait_for_action",
                "data": {
                    "player_id": player_id,
                    "timeout": None,
                },
            },
        )
    )
