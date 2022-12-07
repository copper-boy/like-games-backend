from db.session import session as sessionmaker
from misc import router
from schemas import WSEventSchema
from structures.enums import PlayerActionEnum
from structures.ws import WSConnection
from utils import helpers


@router.game(to_filter="check")
async def check_handler(data: WSEventSchema, ws: WSConnection) -> None:
    async with sessionmaker.begin() as session:
        s = await helpers.get_session_with_raise(session=session, session_id=ws.session_id)
        player, last_player = helpers.get_player_with_last_player(
            session=session, player_id=ws.player_id, last_player=s.last_player
        )
        helpers.release_check_or_raise(
            player=player,
            current_player=s.current_player,
            big_blind_position=s.big_blind_position,
            last_action=s.last_player_action,
            last_player=last_player,
        )

        to_check = await helpers.do_check()
        await helpers.release_action(
            session=session,
            session_id=s.id,
            pot=s.pot,
            player_id=player.id,
            bet=to_check,
            action=PlayerActionEnum.check,
        )

    answer_event = WSEventSchema(
        event="game",
        payload={
            "to_filter": data.payload.to_filter,
            "data": {
                "action": PlayerActionEnum.check,
                "bet": 0,
                "current_player": s.current_player,
            },
        },
    )
    await ws.manager.broadcast_json(event=answer_event)
