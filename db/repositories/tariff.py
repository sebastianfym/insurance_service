from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from config import settings
from db.models.tariff import Tariff
from src.schemas.tariff import TariffCreate


class TariffRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_tariff(self, tariff: TariffCreate):
        tariff = Tariff(
            date=tariff.date,
            cargo_type=tariff.cargo_type,
            rate=tariff.rate,
        )
        self.session.add(tariff)
        await self.session.commit()
        await self.session.refresh(tariff)