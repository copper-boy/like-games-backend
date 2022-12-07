from enum import Enum


class WSEventEnum(str, Enum):
    game = "game"
    helper = "helper"
    server_side = "server_side"
    error = "error"
    server_error = "server_error"


class RegistrationTypeEnum(str, Enum):
    provided = "provided"
    telegram = "telegram"


class CardPositionEnum(str, Enum):
    deck = "deck"
    player = "player"
    table = "table"


class RoundTypeEnum(str, Enum):
    preflop = "preflop"
    flop = "flop"
    river = "river"
    turn = "turn"
    showdown = "showdown"


class PlayerActionEnum(str, Enum):
    unknown = "unknown"
    fold = "fold"
    check = "check"
    call = "call"
    bet = "bet"
    up = "up"
    allin = "allin"
