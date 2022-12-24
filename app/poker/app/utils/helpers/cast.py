from __future__ import annotations

from orm import CardModel, PlayerModel
from schemas import CardSchema, PlayerSchema


def cards_to_pydantic(cards: list[CardModel]) -> list[CardSchema]:
    to_return: list[CardSchema] = []
    for card in cards:
        to_return.append(CardSchema.from_orm(card))

    return to_return


def players_to_pydantic(players: list[PlayerModel], exclude: int) -> list[PlayerSchema]:
    to_return: list[PlayerSchema] = []
    for player in players:
        if player.id == exclude:
            continue
        to_return.append(PlayerSchema.from_orm(player))

    return to_return
