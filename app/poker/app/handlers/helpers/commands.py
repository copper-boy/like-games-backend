from core import tools
from misc import router
from schemas import WSEventSchema
from structures.ws import WSConnection


@router.helper(to_filter="commands")
async def commands_handler(data: WSEventSchema, ws: WSConnection) -> None:
    to_answer: list[dict] = []
    for event_name, observer in router.observers.items():
        for handler in observer.handlers:
            to_append = {
                "event": event_name,
                "to_filter": handler.to_filter,
            }
            to_answer.append(to_append)

    answer_event = WSEventSchema(
        event="helper",
        payload={"to_filter": "commands", "data": to_answer},
    )

    await ws.manager.personal_json(event=answer_event, connection=ws)
