from enum import Enum


class EventEnum(str, Enum):
    error = "like_error"
    game = "like_game"
    helper = "like_helper"
    server = "like_server"


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
