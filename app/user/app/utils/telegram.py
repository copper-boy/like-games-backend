import hashlib
import hmac
import time

from starlette.datastructures import QueryParams

from core.config import get_telegram_settings
from schemas import IntegrationTelegramOAuth2ResponseSchema
from structures.exceptions import NotTelegramDataError, TelegramDataIsOutdatedError

ONE_DAY_IN_SECONDS = 86400


def verify_telegram_authentication(query: QueryParams) -> IntegrationTelegramOAuth2ResponseSchema:
    request_data = dict(query)

    received_hash = request_data.get("hash")
    auth_date = request_data.get("auth_date")

    request_data.pop("hash", None)
    request_data_alphabetical_order = dict(
        sorted(
            request_data.items(),
            key=lambda x: x[0],
        )
    )

    data_check_string = []

    for key, value in request_data_alphabetical_order.items():
        data_check_string.append(f"{key}={value}")

    data_check_string = "\n".join(data_check_string)

    secret_key = hashlib.sha256(get_telegram_settings().TELEGRAM_BOT_API_TOKEN.encode()).digest()
    _hash = hmac.new(
        secret_key,
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()

    unix_time_now = int(time.time())
    unix_time_auth_date = int(auth_date)

    if unix_time_now - unix_time_auth_date > ONE_DAY_IN_SECONDS:
        raise TelegramDataIsOutdatedError(
            "Authentication data is outdated. Authentication was received more than day ago."
        )

    if _hash != received_hash:
        raise NotTelegramDataError(
            "This is not a Telegram data. Hash from recieved authentication data does not match"
            "with calculated hash based on bot token."
        )

    return IntegrationTelegramOAuth2ResponseSchema.parse_obj(request_data)
