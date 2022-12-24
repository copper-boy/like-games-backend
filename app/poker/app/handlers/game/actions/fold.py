from __future__ import annotations

from db.session import session as sessionmaker
from likeevents import LikeF, LikeRouter
from schemas import EventSchema
from structures.enums import PlayerActionEnum
from structures.ws import WS
from utils import helpers

router = LikeRouter()
path = "gameDoFold"


@router.like_game(LikeF.path == path)
async def fold_handler(event: EventSchema, ws: WS) -> None:
    """
    Executes the fold action

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
        player = await helpers.get_player_by_id(session=session, player_id=ws.player_id)

        helpers.release_or_raise(player=player, current_player=s.current_player)

        to_fold = await helpers.do_fold(session=session, player=player)
        await helpers.release_action(
            session=session,
            session_id=s.id,
            round_bet=player.round_bet,
            max_bet=s.max_bet,
            pot=s.pot,
            player_id=player.id,
            bet=to_fold,
            action=PlayerActionEnum.fold,
            ws=ws,
        )
