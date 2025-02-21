import asyncpg
from asyncpg import Pool
from loguru import logger

from database import PgConParams


class PG:
    _pool: Pool

    def __init__(self, conn_params: PgConParams):
        self.conn_params = conn_params

    async def initialize(self):
        logger.info('Connecting pg pool')
        self._pool = await asyncpg.create_pool(**self.conn_params.model_dump(exclude_none=True))

    async def shutdown(self):
        logger.info('Disconnecting pg pool')
        self._pool.terminate()

    def connected(self):
        return not self._pool.is_closing()