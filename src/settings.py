from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    # Postgresql settings
    PG_HOST: str = Field(default='localhost')
    PG_PORT: int = Field(default=5432)
    PG_USER: str = Field(default='')
    PG_PASSWORD: str = Field(default='')
    PG_DB: str = Field(default='')

    # asyncpg pool settings
    PG_POOL_MIN_SIZE: int = Field(default=10)
    PG_POOL_MAX_SIZE: int = Field(default=100)
    PG_POOL_MAX_QUERIES: int = Field(default=10000)
    PG_POOL_CONNECTION_LIFETIME: float = Field(default=360.0)

    @property
    def get_pg_url(self) -> str:
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"


settings = Settings()