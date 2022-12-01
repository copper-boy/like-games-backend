from fastapi.exceptions import HTTPException


class NotTelegramDataError(HTTPException):
    def __init__(self, status_code: int = 404, *args: tuple, **kwargs: dict) -> None:
        super(NotTelegramDataError, self).__init__(status_code=status_code, *args, **kwargs)


class TelegramDataIsOutdatedError(HTTPException):
    def __init__(self, status_code: int = 400, *args: tuple, **kwargs: dict) -> None:
        super(TelegramDataIsOutdatedError, self).__init__(status_code=status_code, *args, **kwargs)
