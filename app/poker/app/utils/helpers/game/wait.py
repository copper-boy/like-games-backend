from __future__ import annotations

from asyncio import sleep

from schemas import EventSchema
from ws import WSManager


async def wait_for_action(manager: WSManager, player_id: int) -> None:
    await manager.broadcast_json(
        event=EventSchema(
            event="game", payload={"to_filter": "wait_for_action", "data": {"timeout": 10}}
        )
    )
    await sleep(10)

    await manager.broadcast_json(
        event=EventSchema(
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
