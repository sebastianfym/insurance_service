from typing import List, ClassVar
from pydantic_settings import BaseSettings
from loguru import logger
from pydantic import computed_field, Field

class Settings(BaseSettings):
    ALLOWED_METHODS: List[str] = Field(default_factory=lambda: ["GET", "POST", "PATCH", "DELETE"])
    ALLOWED_HEADERS: List[str] = Field(default_factory=lambda: ["Content-Type", "Authorization", "Accept", "X-Requested-With"])
    ALLOWED_ORIGINS: str = "*"


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def base_url(self) -> str:
        return f"{self.SERVER_HOST}:{self.SERVER_PORT}"


class PostgresConfig(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @computed_field
    def db_uri(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class LoggerConfig(BaseSettings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        logger.add(
            self.LOG_FILE,
            format=self.LOG_FORMAT,
            level=self.LOG_LEVEL,
            rotation=self.LOG_ROTATION,
            compression=self.LOG_COMPRESSION,
            serialize=self.LOG_SERIALIZE
        )

    LOG_FILE: str = "motivation_service.log"
    LOG_FORMAT: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    LOG_LEVEL: str = "DEBUG"
    LOG_ROTATION: str = "10 MB"
    LOG_COMPRESSION: str = "zip"
    LOG_SERIALIZE: bool = True

    logger: ClassVar = logger

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
postgres_config = PostgresConfig()
logger_config = LoggerConfig()
