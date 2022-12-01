class BaseGameError(Exception):
    """
    Serves as a parent for exceptions that are raised in the game.
    """


class DeckError(BaseGameError):
    """
    Serves as a parent for exceptions that are raised in deck actions.
    """


class NotAcceptablePositionError(DeckError):
    """
    Occurs when an application receives a command to deal cards, and
    `CardPositionEnum.deck` was passed to the card position.
    """
