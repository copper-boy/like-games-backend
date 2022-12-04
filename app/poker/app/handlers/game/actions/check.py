from core import tools
from db.session import session as sessionmaker
from schemas import WSEventSchema
from structures.enums import PlayerActionEnum
from structures.ws import WSConnection
from utils import action, bet, can_release, helpers


async def check_handler(event: WSEventSchema, websocket: WSConnection) -> None:
    async with sessionmaker.begin() as session:
        s = await helpers.get_session_with_raise(session=session, session_id=websocket.session_id)
        player, last_player = helpers.get_player_with_last_player(
            session=session, player_id=websocket.player_id, last_player=s.last_player
        )
        can_release.release_check_or_raise(
            player=player,
            current_player=s.current_player,
            big_blind_position=s.big_blind_position,
            last_action=s.last_player_action,
            last_player=last_player,
        )

        to_check = bet.do_check()
        await action.release_action(
            session=session,
            session_id=s.id,
            pot=s.pot,
            player_id=player.id,
            bet=to_check,
            action=PlayerActionEnum.check,
        )

    answer_event = WSEventSchema(
        command=event.command,
        payload={
            "action": PlayerActionEnum.check,
            "bet": 0,
            "current_player": s.current_player,
        },
    )
    manager = tools.ws_managers.get(websocket.session_id)
    await manager.broadcast_json(event=answer_event)
