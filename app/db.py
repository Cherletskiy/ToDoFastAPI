from contextlib import asynccontextmanager
import asyncpg
from asyncpg.pool import Pool
from typing import Optional
import os
from dotenv import load_dotenv
from app.logging_config import get_logger

logger = get_logger(__name__)

load_dotenv()

_db_pool: Optional[Pool] = None

DSN = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

async def create_pool() -> None:
    """Инициализация пула соединений с базой данных."""
    global _db_pool
    try:
        _db_pool = await asyncpg.create_pool(
            dsn=DSN,
            min_size=1,
            max_size=10,
            max_inactive_connection_lifetime=300.0
        )
        logger.info(f"Пул соединений создан: host={os.getenv('DB_HOST')}, db={os.getenv('DB_NAME')}")
        logger.debug(f"Параметры пула: min_size=1, max_size=10, lifetime=300s")
    except asyncpg.exceptions.PostgresConnectionError as e:
        logger.error(f"Ошибка подключения к базе данных: host={os.getenv('DB_HOST')}, db={os.getenv('DB_NAME')}, ошибка={e}")
        raise
    except Exception as e:
        logger.critical(f"Критическая ошибка при создании пула: host={os.getenv('DB_HOST')}, db={os.getenv('DB_NAME')}")
        logger.exception("Подробности ошибки")
        raise

async def get_pool() -> Pool:
    """Получение пула или создание его, если он еще не создан."""
    global _db_pool
    if _db_pool is None:
        await create_pool()
    return _db_pool

async def close_pool() -> None:
    """Закрытие пула соединений с базой данных."""
    global _db_pool
    if _db_pool is not None:
        await _db_pool.close()
        logger.info(f"Пул соединений закрыт: host={os.getenv('DB_HOST')}, db={os.getenv('DB_NAME')}")
        _db_pool = None

@asynccontextmanager
async def get_connection():
    """Контекстный менеджер для получения и освобождения соединения."""
    pool = await get_pool()
    logger.debug("Получение соединения из пула")
    connection = await pool.acquire()
    try:
        yield connection
    finally:
        logger.debug("Освобождение соединения")
        await pool.release(connection)