from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from config import settings
from db.repositories.insurance import InsuranceRepository
from src.schemas.insurance import Insurance


class InsuranceUtilitiesService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_insurance_cost(self, insurance_data: Insurance) -> float:
        insurance_repository = InsuranceRepository(self.session)
        rate_record = await insurance_repository.get_rate(insurance_data)

        if not rate_record:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Rate not found for the given cargo type and date")

        insurance_cost = insurance_data.declared_value * rate_record.rate
        return insurance_cost

