import os
from datetime import datetime

from typing import List, Dict, Union, Any
import json
from fastapi import UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db.repositories.tariff import TariffRepository
from src.schemas.tariff import TariffCreate


class TariffUtilitiesService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_data_file(self, file: File) -> Union[dict, list]:
        data = json.loads(await file.read())
        return data

    async def upload_tariff(self, file: File):
        tariff_repository = TariffRepository(self.session)

        data = await self.get_data_file(file)

        for date_str, tariffs in data.items():
            for tariff in tariffs:
                tariff_data = TariffCreate(
                    date=datetime.strptime(date_str, "%Y-%m-%d").date(),
                    cargo_type=tariff["cargo_type"],
                    rate=float(tariff["rate"].replace(",", "."))
                )
                await tariff_repository.create_tariff(tariff=tariff_data)