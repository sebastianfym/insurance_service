from enum import Enum

class LogType(Enum):
    TARIFF = "tariff"
    USER = "user"

class TariffFilter(Enum):
    DATE = "date"