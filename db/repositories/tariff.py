from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.tariff import Tariff
from src.enums.enum import TariffFilter
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

    async def get_tariff(self, tariff_id: int) -> Tariff:
        stmt = select(Tariff).where(Tariff.id == tariff_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def edit_tariff(self, tariff_id: int, updated_data: dict) -> Tariff:
        tariff = await self.get_tariff(tariff_id)
        if not tariff:
            return None
        for key, value in updated_data.items():
            if value == None:
                value = getattr(tariff, key)
            if key == TariffFilter.DATE.value:
                value = datetime.strptime(value, '%Y-%m-%d').date()
            setattr(tariff, key, value)
        await self.session.commit()
        await self.session.refresh(tariff)
        return tariff

    async def delete_tariff(self, tariff_id: int) -> bool:
        tariff = await self.get_tariff(tariff_id)
        if not tariff:
            return False
        await self.session.delete(tariff)
        await self.session.commit()
        return True