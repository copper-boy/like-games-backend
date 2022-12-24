from __future__ import annotations


class BaseGameError(Exception):
    """
    Serves as a parent for exceptions that are raised in the game.
    """


class DeckError(BaseGameError):
    """
    Serves as a parent for exceptions that are raised in deck actions.
    """
