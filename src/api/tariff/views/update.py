from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from config import oauth2_scheme
from db.db_service import get_session
from src.api.tariff.router import router
from src.schemas.tariff import TariffEdit, Tariff
from src.services.tariff import TariffUtilitiesService


@router.patch("/{tariff_id}", status_code=HTTP_200_OK, response_model=Tariff, summary="Update tariff")
async def update_tariff(tariff_id: int, tariff_data: TariffEdit, session: AsyncSession = Depends(get_session),
                        token: str = Depends(oauth2_scheme)):
    tariff_service = TariffUtilitiesService(session)
    tariff = await tariff_service.edit_tariff(tariff_id, tariff_data, token)
    return {"status_code": HTTP_200_OK, "detail": f"{Tariff.from_orm(tariff)}"}