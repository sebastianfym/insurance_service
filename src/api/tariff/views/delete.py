from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from config import oauth2_scheme
from db.db_service import get_session
from src.api.tariff.router import router
from src.services.tariff import TariffUtilitiesService


@router.delete("/{tariff_id}", status_code=HTTP_200_OK, summary="Delete tariff")
async def delete_tariff(tariff_id: int, session: AsyncSession = Depends(get_session),
                        token: str = Depends(oauth2_scheme)):
    tariff_service = TariffUtilitiesService(session)
    await tariff_service.delete_tariff(tariff_id, token)
    return {"status_code": HTTP_200_OK, "detail": "Tariff was delete"}