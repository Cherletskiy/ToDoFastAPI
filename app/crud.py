from typing import List, Dict, Any, Optional
from app.db import get_connection
from app.logging_config import get_logger
from datetime import datetime


logger = get_logger(__name__)

async def create_task(
    title: str,
    description: Optional[str] = None,
    due_date: Optional[datetime] = None,
    status: str = "pending"
) -> int:
    """Создание новой задачи."""

    query = """
            INSERT INTO tasks (title, description, due_date, status)
            VALUES ($1, $2, $3, $4)
            RETURNING id
        """

    async with get_connection() as conn:
        try:
            task_id = await conn.fetchval(query, title, description, due_date, status)
            logger.info(f"Создана задача: id={task_id}, title={title}")
            return task_id
        except Exception as e:
            logger.error(f"Ошибка при создании задачи: title={title}, ошибка={e}")
            raise


async def get_task(task_id: int) -> Optional[Dict[str, Any]]:
    """Получение задачи по ID."""
    query = """
        SELECT id, title, description, created_at, due_date, status
        FROM tasks
        WHERE id = $1
    """
    async with get_connection() as conn:
        try:
            task = await conn.fetchrow(query, task_id)
            if task:
                logger.debug(f"Получена задача: id={task_id}")
                return dict(task)
            logger.warning(f"Задача не найдена: id={task_id}")
            return None
        except Exception as e:
            logger.error(f"Ошибка при получении задачи: id={task_id}, ошибка={e}")
            raise


async def get_tasks(
    status: Optional[str] = None,
    due_date_from: Optional[datetime] = None,
    due_date_to: Optional[datetime] = None
) -> List[Dict[str, Any]]:
    """Получение списка задач с фильтрами."""
    query = """
        SELECT id, title, description, created_at, due_date, status
        FROM tasks
        WHERE 1=1
    """
    params = []
    param_counter = 1

    if status:
        query += f" AND status = ${param_counter}"
        params.append(status)
        param_counter += 1
    if due_date_from:
        query += f" AND due_date >= ${param_counter}"
        params.append(due_date_from)
        param_counter += 1
    if due_date_to:
        query += f" AND due_date <= ${param_counter}"
        params.append(due_date_to)
        param_counter += 1

    async with get_connection() as conn:
        try:
            tasks = await conn.fetch(query, *params)
            logger.info(f"Получено {len(tasks)} задач с фильтрами: status={status}, due_date_from={due_date_from}, due_date_to={due_date_to}")
            return [dict(task) for task in tasks]
        except Exception as e:
            logger.error(f"Ошибка при получении списка задач: ошибка={e}")
            raise


async def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    due_date: Optional[datetime] = None,
    status: Optional[str] = None
) -> bool:
    """Обновление задачи."""
    updates = []
    params = []
    param_counter = 1

    if title is not None:
        updates.append(f"title = ${param_counter}")
        params.append(title)
        param_counter += 1
    if description is not None:
        updates.append(f"description = ${param_counter}")
        params.append(description)
        param_counter += 1
    if due_date is not None:
        updates.append(f"due_date = ${param_counter}")
        params.append(due_date)
        param_counter += 1
    if status is not None:
        updates.append(f"status = ${param_counter}")
        params.append(status)
        param_counter += 1

    if not updates:
        logger.warning(f"Нет данных для обновления задачи: id={task_id}")
        return False

    query = f"""
        UPDATE tasks
        SET {', '.join(updates)}
        WHERE id = ${param_counter}
        RETURNING id
    """
    params.append(task_id)

    async with get_connection() as conn:
        try:
            result = await conn.fetchval(query, *params)
            if result:
                logger.info(f"Обновлена задача: id={task_id}")
                return True
            logger.warning(f"Задача не найдена для обновления: id={task_id}")
            return False
        except Exception as e:
            logger.error(f"Ошибка при обновлении задачи: id={task_id}, ошибка={e}")
            raise

async def delete_task(task_id: int) -> bool:
    """Удаление задачи."""
    query = """
        DELETE FROM tasks
        WHERE id = $1
        RETURNING id
    """
    async with get_connection() as conn:
        try:
            result = await conn.fetchval(query, task_id)
            if result:
                logger.info(f"Удалена задача: id={task_id}")
                return True
            logger.warning(f"Задача не найдена для удаления: id={task_id}")
            return False
        except Exception as e:
            logger.error(f"Ошибка при удалении задачи: id={task_id}, ошибка={e}")
            raise