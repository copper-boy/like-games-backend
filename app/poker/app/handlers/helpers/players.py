from core import tools
from db.session import session as sessionmaker
from orm import PlayerModel
from schemas import WSEventSchema
from structures.ws import WSConnection
from utils import helpers


async def players_handler(event: WSEventSchema, websocket: WSConnection) -> None:
    async with sessionmaker.begin() as session:
        players = await tools.store.game_player_accessor.get_players_by(
            session=session, where=(PlayerModel.session_id == websocket.session_id)
        )

    session_players = helpers.players_to_pydantic(players=players, exclude=websocket.player_id)
    answer_event = WSEventSchema(command=event.command, payload={"players": session_players})
    manager = tools.ws_managers.get(websocket.session_id)
    await manager.personal_json(event=answer_event, connection=websocket)
