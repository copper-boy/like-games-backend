from random import shuffle

from schemas.game import LogicCardSchema, LogicDeckSchema
from store.base import BaseAccessor
from structures.constants import CARD_RANK, CARD_SUIT


class DeckAccessor(BaseAccessor):
    def __generate_deck(self) -> list[LogicCardSchema]:
        to_return: list[LogicCardSchema] = []
        for suit in CARD_SUIT:
            for rank in CARD_RANK:
                to_return.append(LogicCardSchema(rank=rank, suit=suit))

        return to_return

    def make_deck(self, with_shuffle: bool = False) -> LogicDeckSchema:
        to_return = LogicDeckSchema(deck=self.__generate_deck())

        if with_shuffle:
            shuffle(to_return.deck)

        return to_return
