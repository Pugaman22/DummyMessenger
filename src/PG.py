import asyncpg
from asyncpg import Pool
from loguru import logger

from database import PgConParams, PgPoolParams


class PG:
    """Класс для управления соединением с PostgreSQL через пул."""
    _pool: Pool

    def __init__(self, conn_params: PgConParams):
        self.conn_params = conn_params

    async def initialize(self):
        """Создаёт пул соединений и создаёт таблицу, если её нет."""
        logger.info("Connecting...")

        self._pool = await asyncpg.create_pool(**self.conn_params.model_dump(exclude_none=True))

        async with self._pool.acquire() as conn:
            await conn.execute("""
                   CREATE TABLE IF NOT EXISTS messages (
                       id SERIAL PRIMARY KEY,
                       user_name TEXT NOT NULL,
                       text TEXT NOT NULL,
                       created_at TIMESTAMP DEFAULT now(),
                       message_index INTEGER NOT NULL,
                       user_message_count INTEGER NOT NULL
                   );
               """)
        logger.info("Database initialized.")

    async def shutdown(self):
        """Закрывает пул соединений."""
        logger.info("Closing connection...")
        await self._pool.close()

    def connected(self) -> bool:
        """Проверяет, открыто ли соединение с БД."""
        return not self._pool.is_closing()

    async def fetch(self, query: str, *args):
        """Выполняет SELECT-запрос и возвращает данные."""
        async with self._pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def execute(self, query: str, *args):
        """Выполняет запрос (INSERT, UPDATE, DELETE)."""
        async with self._pool.acquire() as conn:
            return await conn.execute(query, *args)


pg_pool = PG(PgPoolParams())
