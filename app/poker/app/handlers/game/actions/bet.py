from core import tools
from db.session import session as sessionmaker
from misc import router
from schemas import WSEventSchema
from structures.enums import PlayerActionEnum
from structures.exceptions import WSCommandError
from structures.ws import WSConnection
from utils import action, bet, can_release, helpers


@router.action(to_filter="bet")
async def bet_handler(data: WSEventSchema, ws: WSConnection) -> None:
    ws_bet = data.payload.data.get("bet")

    async with sessionmaker.begin() as session:
        s = await helpers.get_session_with_raise(session=session, session_id=ws.session_id)
        player = await helpers.get_player_by_id(session=session, player_id=ws.player_id)

        if ws_bet >= player.game_chips:
            raise WSCommandError

        can_release.release_bet_or_raise(
            player=player,
            current_player=s.current_player,
            big_blind=s.game.big_blind,
            bet=ws_bet,
        )

        to_bet = bet.do_bet(session=session, player=player, bet=ws_bet)
        await action.release_action(
            session=session,
            session_id=s.id,
            pot=s.pot,
            player_id=player.id,
            bet=to_bet,
            action=PlayerActionEnum.bet,
        )

    answer_event = WSEventSchema(
        event="action",
        payload={
            "to_filter": data.payload.to_filter,
            "data": {
                "action": PlayerActionEnum.bet,
                "bet": to_bet,
                "current_player": s.current_player,
            },
        },
    )
    await ws.manager.broadcast_json(event=answer_event)
