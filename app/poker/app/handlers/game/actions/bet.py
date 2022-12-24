from __future__ import annotations

from db.session import session as sessionmaker
from likeevents import LikeF, LikeRouter
from schemas import EventSchema
from structures.enums import PlayerActionEnum
from structures.exceptions import WSCommandError
from structures.ws import WS
from utils import helpers

router = LikeRouter()
path = "gameDoBet"


@router.like_game(LikeF.path == path)
async def bet_handler(event: EventSchema, ws: WS) -> None:
    """
    Executes the bet action

    :param event:
      required data received from client
    :param ws:
      constructed ws connection
    :return:
      None
    :raise WSCommandError:
      when the player cannot take this action
    :raise WSStateError:
      when game not started
    """

    ws_bet = event.payload.data.get("bet")

    async with sessionmaker.begin() as session:
        s = await helpers.get_session_with_raise(session=session, session_id=ws.session_id)
        player = await helpers.get_player_by_id(session=session, player_id=ws.player_id)

        if ws_bet >= player.game_chips:
            raise WSCommandError

        helpers.release_bet_or_raise(
            player=player,
            current_player=s.current_player,
            big_blind=s.game.big_blind,
            bet=ws_bet,
        )

        to_bet = await helpers.do_bet(session=session, player=player, bet=ws_bet)
        await helpers.release_action(
            session=session,
            session_id=s.id,
            round_bet=player.round_bet,
            max_bet=s.max_bet,
            pot=s.pot,
            player_id=player.id,
            bet=to_bet,
            action=PlayerActionEnum.bet,
            ws=ws,
        )
