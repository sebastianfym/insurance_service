from typing import Optional, Union

from pydantic import BaseModel, field_validator
from datetime import datetime, date

class TariffBase(BaseModel):
    date: Optional[Union[date, str]] = None
    cargo_type: Optional[str] = None
    rate: Optional[float] = None

    @field_validator("date", mode="before")
    def validate_date(cls, value):
        if isinstance(value, date):
            return value.isoformat()
        elif isinstance(value, datetime):
            return value.date().isoformat()
        return value


class TariffCreate(TariffBase):
    pass

class Tariff(TariffBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True

class TariffEdit(TariffBase):
    pass