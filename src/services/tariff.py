import os
from datetime import datetime

from typing import List, Dict, Union, Any
import json
from fastapi import UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db import Tariff
from db.repositories.tariff import TariffRepository
from db.repositories.user import UserRepository
from src.enums.enum import LogType, LogAction
from src.schemas.tariff import TariffCreate, TariffEdit
from src.services.auth import AuthUtilitiesService
from src.services.kafka import send_to_kafka_async


class TariffUtilitiesService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_data_file(self, file: File) -> Union[dict, list]:
        data = json.loads(await file.read())
        return data

    async def upload_tariff(self, file: File, token:str):
        logg = await self.log_action(token, LogAction.UPLOAD)
        await send_to_kafka_async(topic="Edit", key=LogType.TARIFF.value, value=logg)
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

    async def delete_tariff(self, tariff_id: int, token:str):
        logg = await self.log_action(token, LogAction.DELETE)
        await send_to_kafka_async(topic="Edit", key=LogType.TARIFF.value, value=logg)
        tariff_repository = TariffRepository(self.session)
        await tariff_repository.delete_tariff(tariff_id)

    async def edit_tariff(self, tariff_id, tariff_data: TariffEdit, token:str) -> Tariff:
        logg = await self.log_action(token, LogAction.EDIT)
        await send_to_kafka_async(topic="Edit", key=LogType.TARIFF.value, value=logg)
        tariff_repository = TariffRepository(self.session)
        return await tariff_repository.edit_tariff(tariff_id, tariff_data.dict())

    async def log_action(self, token:str, action: LogAction) -> dict:
        payload = AuthUtilitiesService.verify_token(token)
        user_repository = UserRepository(self.session)
        user = await user_repository.get_current_user(payload)
        logg = {"action": f"{action.value} tariff", "date": datetime.now()}
        if user is not None:
            logg = {"action": f"User: {user.id} edit tariff", "date": datetime.now()}
        return logg