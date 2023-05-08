from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase
from uvicorn.config import logger

from config import settings


class AsyncDataBase:
    client: AsyncIOMotorClient = None


ASYNC_DB = AsyncDataBase()


async def connect_to_mongo():
    ASYNC_DB.client = AsyncIOMotorClient(settings.MONGODB_URI)
    logger.info("mongodb connected.")


async def close_mongo_connection():
    ASYNC_DB.client.close()
    logger.info("mongodb closed.")


async def get_mongo_database() -> AgnosticDatabase:
    return ASYNC_DB.client[settings.MONGODB_DB_NAME]
