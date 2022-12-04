from core import tools
from schemas import CommandPayloadSchema, WSEventSchema
from structures.command import Command
from structures.loader import Loader
from structures.ws import WSConnection

_loader = Loader()


async def commands_handler(event: WSEventSchema, websocket: WSConnection) -> None:
    payload = CommandPayloadSchema.parse_obj(event.payload)

    if payload.with_descriptions:
        exclude = None
    else:
        exclude = {"description"}

    to_answer: list[Command] = []
    for command in tools.store.ws_accessor.handlers.keys():
        loaded = _loader.load_to_dict(obj=command, exclude=exclude)
        to_answer.append(loaded)

    answer_event = WSEventSchema(command=event.command, payload={"descriptions": to_answer})
    manager = tools.ws_managers.get(websocket.session_id)
    await manager.personal_json(event=answer_event, connection=websocket)
