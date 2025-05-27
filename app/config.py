from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_HOST: str = 'localhost'
    DB_PORT: int
    DB_USER: str = 'postgres'
    DB_PASS: Annotated[str, Field(alias="DB_PASSWORD")]

    REDIS_HOST: str
    REDIS_PORT: int = 6379

    DATE_FORMAT: str = "%d.%m.%Y"

    MODE: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()
