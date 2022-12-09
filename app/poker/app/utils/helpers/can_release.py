from orm import PlayerModel
from structures.enums import PlayerActionEnum
from structures.exceptions import WSCommandError


def release_or_raise(player: PlayerModel, current_player: int) -> None:
    if (player.is_allin or player.is_folded) or current_player != player.id:
        if current_player != player.id:
            raise WSCommandError("You not the current player")
        else:
            raise WSCommandError(f"You already in {'fold' if player.is_folded else 'allin'}")


def release_bet_or_raise(
    player: PlayerModel, current_player: int, big_blind: int, bet: int
) -> None:
    release_or_raise(player=player, current_player=current_player)

    if bet < big_blind:
        raise WSCommandError(f"Bet {bet} less than {big_blind=}")


def release_check_or_raise(
    player: PlayerModel,
    current_player: int,
    big_blind_position: int,
    last_action: PlayerActionEnum,
    last_player: PlayerModel,
) -> None:
    release_or_raise(player=player, current_player=current_player)

    if (
        player.last_bet != last_player.last_bet
        or (player.id != big_blind_position and player.last_bet != last_player.last_bet)
        or (last_action != PlayerActionEnum.check)
    ):
        raise WSCommandError("Unable to complete check")


def release_up_or_raise(
    player: PlayerModel, current_player: int, big_blind: int, bet: int
) -> None:
    release_bet_or_raise(
        player=player,
        current_player=current_player,
        big_blind=big_blind,
        bet=bet,
    )

    if bet == big_blind:
        raise WSCommandError("Raise must be > big blind bet")
