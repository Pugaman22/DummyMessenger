from pydantic import BaseModel, Field

from settings import settings


class PgConParams(BaseModel):
    password: str | None = Field(default=settings.PG_PASSWORD)
    host: str | None = Field(default=settings.PG_HOST)
    port: int | None = Field(default=settings.PG_PORT)
    user: str | None = Field(default=settings.PG_USER)
    database: str | None = Field(default=settings.PG_DB)
    dsn: str | None = Field(default=None)


class PgPoolParams(PgConParams):
    min_size: int = Field(default=settings.PG_POOL_MIN_SIZE)
    max_size: int = Field(default=settings.PG_POOL_MAX_SIZE)
    max_queries: int = Field(default=settings.PG_POOL_MAX_QUERIES)
    max_inactive_connection_lifetime: float = Field(default=settings.PG_POOL_CONNECTION_LIFETIME)
    server_settings: dict | None = Field(default=None)
