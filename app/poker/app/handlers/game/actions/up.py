from db.session import session as sessionmaker
from misc import router
from schemas import WSEventSchema
from structures.enums import PlayerActionEnum
from structures.ws import WSConnection
from utils import helpers


@router.game(to_filter="up")
async def up_handler(data: WSEventSchema, ws: WSConnection) -> None:
    ws_bet = data.payload.data.get("bet")

    async with sessionmaker.begin() as session:
        s = await helpers.get_session_with_raise(session=session, session_id=ws.session_id)
        player, last_player = helpers.get_player_with_last_player(
            session=session, player_id=ws.player_id, last_player=s.last_player
        )

        last_known_round = s.round.type

        helpers.release_up_or_raise(
            player=player,
            current_player=s.current_player,
            big_blind=s.game.big_blind,
            bet=ws_bet,
        )

        to_up = await helpers.do_up(session=session, player=player, bet=ws_bet)
        await helpers.release_action(
            session=session,
            session_id=s.id,
            round_bet=player.round_bet,
            max_bet=s.max_bet,
            pot=s.pot,
            player_id=player.id,
            bet=to_up,
            action=PlayerActionEnum.up,
        )

    round_type = await helpers.next_round_call(session_id=s.id, manager=ws.manager)

    answer_event = WSEventSchema(
        event="game",
        payload={
            "to_filter": data.payload.to_filter,
            "data": {
                "action": PlayerActionEnum.up,
                "bet": to_up,
                "current_player": s.current_player,
            },
        },
    )
    await helpers.with_predicate(
        first_operand=last_known_round,
        second_operand=round_type,
        event=answer_event,
        manager=ws.manager,
    )
