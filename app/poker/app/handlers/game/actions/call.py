from db.session import session as sessionmaker
from misc import router
from schemas import WSEventSchema
from structures.enums import PlayerActionEnum
from structures.ws import WSConnection
from utils import helpers


@router.game(to_filter="call")
async def call_handler(data: WSEventSchema, ws: WSConnection) -> None:
    async with sessionmaker.begin() as session:
        s = await helpers.get_session_with_raise(session=session, session_id=ws.session_id)
        player, last_player = helpers.get_player_with_last_player(
            session=session, player_id=ws.player_id, last_player=s.last_player
        )

        helpers.release_or_raise(player=player, current_player=s.current_player)

        to_call = await helpers.do_call(
            session=session, player=player, last_bet=last_player.last_bet
        )
        await helpers.release_action(
            session=session,
            session_id=s.id,
            round_bet=player.round_bet,
            max_bet=s.max_bet,
            pot=s.pot,
            player_id=player.id,
            bet=to_call,
            action=PlayerActionEnum.call,
        )

    answer_event = WSEventSchema(
        event="game",
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
