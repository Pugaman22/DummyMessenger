from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from loguru import logger

from PG import pg_pool


class MessageRequest(BaseModel):
    user_name: str
    text: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Application starting...')
    await pg_pool.initialize()
    yield
    logger.info('Application shutting down...')
    await pg_pool.shutdown()


app: FastAPI = FastAPI(lifespan=lifespan)


@app.post('/message')
async def message(payload: MessageRequest):
    """Принимает сообщение, сохраняет его в БД и возвращает 10 последних сообщений."""
    try:
        user_count_query = "SELECT COUNT(*) AS user_count FROM messages WHERE user_name = $1"
        last_message = await pg_pool.fetch(user_count_query, payload.user_name)
        user_message_count = last_message[0]['user_count'] + 1

        last_index_query = "SELECT MAX(message_index) AS last_index FROM messages"
        last_message_index = await pg_pool.fetch(last_index_query)
        message_index = (last_message_index[0]['last_index'] or 0) + 1

        # Сохранение сообщения
        insert_query = """
                INSERT INTO messages (user_name, text, created_at, message_index, user_message_count) 
                VALUES ($1, $2, $3, $4, $5)
            """
        await pg_pool.execute(insert_query, payload.user_name, payload.text, datetime.utcnow(), message_index,
                              user_message_count)
        logger.info(f"Message saved: {payload.user_name} - {payload.text}")

        # Получение 10 последних сообщений
        last_messages_query = """
                SELECT user_name, text, created_at, message_index, user_message_count
                FROM messages
                ORDER BY created_at DESC
                LIMIT 10
            """
        last_messages = await pg_pool.fetch(last_messages_query)

        return {"messages": [dict(msg) for msg in last_messages]}

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail={"error": "Internal server error",
                                                     "detail": 'An unexpected error occurred'})
