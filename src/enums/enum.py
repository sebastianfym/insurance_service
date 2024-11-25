from enum import Enum


class LogType(Enum):
    TARIFF = "tariff"
    USER = "user"

class LogAction(Enum):
    EDIT = "edit"
    DELETE = "delete"
    UPLOAD = "upload"

class TariffFilter(Enum):
    DATE = "date"

