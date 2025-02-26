import asyncio
import random
import time

from loguru import logger
from aiohttp import ClientSession


COROUTINES = 50
REQUESTS_PER_COROUTINE = 100
TOTAL_REQUESTS = COROUTINES * REQUESTS_PER_COROUTINE
REPLICA_URLS = ('http://127.0.0.1:8008/message', 'http://127.0.0.1:8009/message')

USERS = [f"User{i}" for i in range(10)]


async def send_request(session: ClientSession, url: str) -> dict:
    """POST запрос с сообщением на указанный URL."""
    payload = {
        "user_name": random.choice(USERS),
        "text": f"This message is from {random.choice(USERS)}!"
    }
    async with session.post(url=url, json=payload) as response:
        return await response.json()


async def make_session() -> None:
    """Создаёт сессию и отправляет 100 запросов."""
    async with ClientSession() as session:
        for _ in range(REQUESTS_PER_COROUTINE):
            url = random.choice(REPLICA_URLS)
            try:
                response = await send_request(session, url)
                # logger.info(f"Response: {response}")
            except Exception as e:
                logger.error(f"Request failed: {e}")


async def main() -> None:

    start_time = time.time()
    await asyncio.gather(* (make_session() for _ in range(COROUTINES)))
    end_time = time.time()

    total_time = end_time - start_time
    avg_request_time = total_time / TOTAL_REQUESTS
    rps = TOTAL_REQUESTS / total_time

    logger.info(f"Total requests: {TOTAL_REQUESTS}")
    logger.info(f"Total time: {total_time:.2f} sec")
    logger.info(f"Avg time per request: {avg_request_time:.4f} sec")
    logger.info(f"Requests per second (RPS): {rps:.2f}")


if __name__ == '__main__':
    asyncio.run(main())


