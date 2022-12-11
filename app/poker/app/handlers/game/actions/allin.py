from db.session import session as sessionmaker
from misc import router
from schemas import WSEventSchema
from structures.enums import PlayerActionEnum
from structures.ws import WSConnection
from utils import helpers


@router.game(to_filter="allin")
async def allin_handler(data: WSEventSchema, ws: WSConnection) -> None:
    """
    Executes the allin action

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
        player = await helpers.get_player_by_id(session=session, player_id=ws.player_id)

        helpers.release_or_raise(player=player, current_player=s.current_player)

        to_allin = await helpers.do_allin(session=session, player=player)
        await helpers.release_action(
            session=session,
            session_id=s.id,
            round_bet=player.round_bet,
            max_bet=s.max_bet,
            pot=s.pot,
            player_id=player.id,
            bet=to_allin,
            action=PlayerActionEnum.allin,
        )
