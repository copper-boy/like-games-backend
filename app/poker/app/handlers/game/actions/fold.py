from core import tools
from db.session import session as sessionmaker
from schemas import WSEventSchema
from structures.enums import PlayerActionEnum
from structures.ws import WSConnection
from utils import action, bet, can_release, helpers


async def fold_handler(event: WSEventSchema, websocket: WSConnection) -> None:
    async with sessionmaker.begin() as session:
        s = await helpers.get_session_with_raise(session=session, session_id=websocket.session_id)
        player = await helpers.get_player_by_id(session=session, player_id=websocket.player_id)

        can_release.release_or_raise(player=player, current_player=s.current_player)

        to_fold = bet.do_fold(session=session, player=player)
        await action.release_action(
            session=session,
            session_id=s.id,
            pot=s.pot,
            player_id=player.id,
            bet=to_fold,
            action=PlayerActionEnum.fold,
        )

    answer_event = WSEventSchema(
        command=event.command,
        payload={
            "action": PlayerActionEnum.fold,
            "bet": 0,
            "current_player": s.current_player,
        },
    )
    manager = tools.ws_managers.get(websocket.session_id)
    await manager.broadcast_json(event=answer_event)
