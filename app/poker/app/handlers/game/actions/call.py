from core import tools
from db.session import session as sessionmaker
from misc import router
from schemas import WSEventSchema
from structures.enums import PlayerActionEnum
from structures.ws import WSConnection
from utils import action, bet, can_release, helpers


@router.action(to_filter="call")
async def call_handler(data: WSEventSchema, ws: WSConnection) -> None:
    async with sessionmaker.begin() as session:
        s = await helpers.get_session_with_raise(session=session, session_id=ws.session_id)
        player, last_player = helpers.get_player_with_last_player(
            session=session, player_id=ws.player_id, last_player=s.last_player
        )

        can_release.release_or_raise(player=player, current_player=s.current_player)

        to_call = bet.do_call(session=session, player=player, last_bet=last_player.last_bet)
        await action.release_action(
            session=session,
            session_id=s.id,
            pot=s.pot,
            player_id=player.id,
            bet=to_call,
            action=PlayerActionEnum.call,
        )

    answer_event = WSEventSchema(
        event="action",
        payload={
            "to_filter": data.payload.to_filter,
            "data": {
                "action": PlayerActionEnum.call,
                "bet": to_call,
                "current_player": s.current_player,
            },
        },
    )
    await ws.manager.broadcast_json(event=answer_event)
