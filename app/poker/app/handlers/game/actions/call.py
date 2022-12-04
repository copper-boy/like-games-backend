from core import tools
from db.session import session as sessionmaker
from schemas import BetPayloadSchema, WSEventSchema
from structures.enums import PlayerActionEnum
from structures.ws import WSConnection
from utils import action, bet, can_release, helpers

from . import allin, bet


async def call_handler(event: WSEventSchema, websocket: WSConnection) -> None:
    async with sessionmaker.begin() as session:
        s = await helpers.get_session_with_raise(session=session, session_id=websocket.session_id)
        player, last_player = helpers.get_player_with_last_player(
            session=session, player_id=websocket.player_id, last_player=s.last_player
        )

        can_release.release_or_raise(player=player, current_player=s.current_player)

        if last_player.last_bet >= player.game_chips:
            return await allin.allin_handler(event=event, websocket=websocket)
        if last_player.last_action == PlayerActionEnum.allin:
            new_event = WSEventSchema(
                command="bet", payload=BetPayloadSchema(bet=last_player.last_bet)
            )
            return await bet.bet_handler(event=new_event, websocket=websocket)

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
        command=event.command,
        payload={
            "action": PlayerActionEnum.call,
            "bet": to_call,
            "current_player": s.current_player,
        },
    )
    manager = tools.ws_managers.get(websocket.session_id)
    await manager.broadcast_json(event=answer_event)
