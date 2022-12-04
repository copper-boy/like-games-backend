from core import tools
from db.session import session as sessionmaker
from schemas import BetPayloadSchema, WSEventSchema
from structures.enums import PlayerActionEnum
from structures.ws import WSConnection
from utils import action, bet, can_release, helpers

from . import allin


async def bet_handler(event: WSEventSchema, websocket: WSConnection) -> None:
    payload = BetPayloadSchema.parse_obj(event.payload)

    async with sessionmaker.begin() as session:
        s = await helpers.get_session_with_raise(session=session, session_id=websocket.session_id)
        player = await helpers.get_player_by_id(session=session, player_id=websocket.player_id)

        if payload.bet >= player.game_chips:
            return await allin.allin_handler(event=event, websocket=websocket)

        can_release.release_bet_or_raise(
            player=player,
            current_player=s.current_player,
            big_blind=s.game.big_blind,
            bet=payload.bet,
        )

        to_bet = bet.do_bet(session=session, player=player, bet=payload.bet)
        await action.release_action(
            session=session,
            session_id=s.id,
            pot=s.pot,
            player_id=player.id,
            bet=to_bet,
            action=PlayerActionEnum.bet,
        )

    answer_event = WSEventSchema(
        command=event.command,
        payload={
            "action": PlayerActionEnum.bet,
            "bet": to_bet,
            "current_player": s.current_player,
        },
    )
    manager = tools.ws_managers.get(websocket.session_id)
    await manager.broadcast_json(event=answer_event)
