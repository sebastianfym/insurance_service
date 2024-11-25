from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from db.db_service import get_session
from src.api.insurance.router import router
from src.schemas.error import ErrorException
from src.schemas.insurance import Insurance
from src.services.insurance import InsuranceUtilitiesService


@router.post("/insurance/", status_code=HTTP_200_OK, summary="Calculate insurance", responses={
                400: {"model": ErrorException, "detail": "unexpected error",
                      "message": "The calculation was not made"}
            })
async def calculate_insurance(insurance_data: Insurance, session: Session = Depends(get_session)):
    insurance_service = InsuranceUtilitiesService(session)
    try:
        insurance_cost = await insurance_service.get_insurance_cost(insurance_data)
        return {"status_code": HTTP_200_OK, "insurance_cost": insurance_cost}
    except Exception as error:
        return HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=error)
