from pydantic import BaseModel
from datetime import date

class TariffBase(BaseModel):
    date: date
    cargo_type: str = None
    rate: float = None

class TariffCreate(TariffBase):
    pass

class Tariff(TariffBase):
    id: int

    class Config:
        from_attributes = True