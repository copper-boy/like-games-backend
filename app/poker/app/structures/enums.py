from enum import Enum


class RegistrationTypeEnum(str, Enum):
    provided = "provided"
    telegram = "telegram"


class CardPositionEnum(str, Enum):
    deck = "deck"
    player = "player"
    table = "table"


class GameTypeEnum(str, Enum):
    texas = "texas"


class RoundTypeEnum(str, Enum):
    preflop = "preflop"
    flop = "flop"
    river = "river"
    turn = "turn"
    showdown = "showdown"


class PlayerActionEnum(str, Enum):
    unknown = "unknown"
    fold = "fold"
    call = "call"
    bet = "bet"
    up = "up"
    allin = "allin"
