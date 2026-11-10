from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):

    APP_NAME: str = "EnterpriseX"
    APP_ENV: str = "development"

    DATABASE_URL: str | None = None
    DATABASE_HOST: str | None = None
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str | None = None
    DATABASE_USER: str | None = None
    DATABASE_PASSWORD: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def sqlalchemy_database_url(self) -> str | URL:
        credentials = (
            self.DATABASE_HOST,
            self.DATABASE_NAME,
            self.DATABASE_USER,
            self.DATABASE_PASSWORD,
        )
        if all(value is not None for value in credentials):
            return URL.create(
                "postgresql+psycopg",
                username=self.DATABASE_USER,
                password=self.DATABASE_PASSWORD,
                host=self.DATABASE_HOST,
                port=self.DATABASE_PORT,
                database=self.DATABASE_NAME,
            )
        if self.DATABASE_URL:
            return self.DATABASE_URL
        raise ValueError(
            "Set DATABASE_URL or all DATABASE_HOST, DATABASE_NAME, "
            "DATABASE_USER, and DATABASE_PASSWORD values."
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
