import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from src.api.tariff.router import router as tariff_router
from src.api.insurance.router import router as insurance_router

from config import settings

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

v1 = APIRouter(prefix="/api/v1")
v1.include_router(tariff_router)
v1.include_router(insurance_router)


app.include_router(v1)
