from __future__ import annotations

from db.session import session as sessionmaker
from likeevents import LikeF, LikeRouter
from schemas import EventSchema
from structures.enums import PlayerActionEnum
from structures.ws import WS
from utils import helpers

router = LikeRouter()
path = "gameDoCall"


@router.like_game(LikeF.path == path)
async def call_handler(event: EventSchema, ws: WS) -> None:
    """
    Executes the call action

    :param event:
      optional data received from client
    :param ws:
      constructed ws connection
    :return:
      None
    :raise WSCommandError:
      when the player cannot take this action
    :raise WSStateError:
      when game not started
    """

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
            ws=ws,
        )
