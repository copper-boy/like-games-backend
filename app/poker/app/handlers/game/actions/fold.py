from db.session import session as sessionmaker
from misc import router
from schemas import WSEventSchema
from structures.enums import PlayerActionEnum
from structures.ws import WSConnection
from utils import helpers


@router.game(to_filter="fold")
async def fold_handler(data: WSEventSchema, ws: WSConnection) -> None:
    async with sessionmaker.begin() as session:
        s = await helpers.get_session_with_raise(session=session, session_id=ws.session_id)
        player = await helpers.get_player_by_id(session=session, player_id=ws.player_id)

        helpers.release_or_raise(player=player, current_player=s.current_player)

        to_fold = await helpers.do_fold(session=session, player=player)
        await helpers.release_action(
            session=session,
            session_id=s.id,
            pot=s.pot,
            player_id=player.id,
            bet=to_fold,
            action=PlayerActionEnum.fold,
        )

    answer_event = WSEventSchema(
        event="game",
        payload={
            "to_filter": data.payload.to_filter,
            "data": {
                "action": PlayerActionEnum.fold,
                "bet": 0,
                "current_player": s.current_player,
            },
        },
    )
    await ws.manager.broadcast_json(event=answer_event)
