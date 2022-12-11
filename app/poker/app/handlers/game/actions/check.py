from db.session import session as sessionmaker
from misc import router
from schemas import WSEventSchema
from structures.enums import PlayerActionEnum
from structures.ws import WSConnection
from utils import helpers


@router.game(to_filter="check")
async def check_handler(data: WSEventSchema, ws: WSConnection) -> None:
    """
    Executes the check action

    :param data:
      optional data received from client
    :param ws:
      constructed websocket connection
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

        helpers.release_check_or_raise(
            player=player,
            current_player=s.current_player,
            big_blind_position=s.big_blind_position,
            last_action=s.last_player_action,
            last_player=last_player,
        )

        to_check = await helpers.do_check()
        await helpers.release_action(
            session=session,
            session_id=s.id,
            round_bet=player.round_bet,
            max_bet=s.max_bet,
            pot=s.pot,
            player_id=player.id,
            bet=to_check,
            action=PlayerActionEnum.check,
        )
