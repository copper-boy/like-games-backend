from enum import Enum


class FilterPathEnum(str, Enum):
    id = "id"
    telegram = "telegram"


class RegistrationTypeEnum(str, Enum):
    provided = "provided"
    telegram = "telegram"
