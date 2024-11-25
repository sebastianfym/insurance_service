from fastapi import Depends, HTTPException

from fastapi import UploadFile, File
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from db.db_service import get_session


from src.api.tariff.router import router
from src.schemas.error import ErrorException
from src.services.tariff import TariffUtilitiesService


@router.post("/upload-tariffs/", status_code=HTTP_200_OK, summary="Upload tariffs", responses={
                400: {"model": ErrorException, "detail": "unexpected error",
                      "message": "The file was not uploaded"}
            })
async def upload_tariffs(file: UploadFile = File(...), session: Session = Depends(get_session)):
    tariff_service = TariffUtilitiesService(session)
    try:
        await tariff_service.upload_tariff(file)
        return {"status_code": HTTP_200_OK, "detail": "Tariffs uploaded successfully"}
    except Exception as error:
        return HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=error)
