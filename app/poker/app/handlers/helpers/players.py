from core import tools
from db.session import session as sessionmaker
from misc import router
from orm import PlayerModel
from schemas import WSEventSchema
from structures.ws import WSConnection
from utils import helpers


@router.helper(to_filter="players")
async def players_handler(data: WSEventSchema, ws: WSConnection) -> None:
    async with sessionmaker.begin() as session:
        players = await tools.store.game_player_accessor.get_players_by(
            session=session, where=(PlayerModel.session_id == ws.session_id)
        )

    answer_event = WSEventSchema(
        event="helper",
        payload={
            "to_filter": "players",
            "data": helpers.players_to_pydantic(players=players, exclude=ws.player_id),
        },
    )
    await ws.manager.broadcast_json(event=answer_event)
