from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db.models.tariff import Tariff
from src.schemas.insurance import Insurance


class InsuranceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_rate(self, insurance_data: Insurance) -> Tariff:
        stmt = await self.session.execute(select(Tariff).where(Tariff.date <= insurance_data.date and Tariff.cargo_type == insurance_data.cargo_type))
        result = stmt.scalar_one_or_none()
        return result
