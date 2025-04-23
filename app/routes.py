from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from app.crud import create_task, get_task, get_tasks, update_task, delete_task
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task_endpoint(task: TaskCreate):
    """Создание новой задачи."""
    try:
        task_id = await create_task(
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            status=task.status
        )
        task_data = await get_task(task_id)
        if task_data:
            logger.info(f"API: Создана задача: id={task_id}")
            return task_data
        raise HTTPException(status_code=500, detail="Не удалось получить созданную задачу")
    except Exception as e:
        logger.error(f"API: Ошибка при создании задачи: {e}")
        raise HTTPException(status_code=500, detail="Ошибка сервера")

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_endpoint(task_id: int):
    """Получение задачи по ID."""
    task = await get_task(task_id)
    if task:
        logger.info(f"API: Получена задача: id={task_id}")
        return task
    logger.warning(f"API: Задача не найдена: id={task_id}")
    raise HTTPException(status_code=404, detail="Задача не найдена")

@router.get("/", response_model=List[TaskResponse])
async def get_tasks_endpoint(
    status: Optional[str] = Query(None, description="Фильтр по статусу"),
    due_date_from: Optional[datetime] = Query(None, description="Срок выполнения от"),
    due_date_to: Optional[datetime] = Query(None, description="Срок выполнения до")
):
    """Получение списка задач с фильтрами."""
    try:
        tasks = await get_tasks(
            status=status,
            due_date_from=due_date_from,
            due_date_to=due_date_to
        )
        logger.info(f"API: Получено {len(tasks)} задач")
        return tasks
    except Exception as e:
        logger.error(f"API: Ошибка при получении списка задач: {e}")
        raise HTTPException(status_code=500, detail="Ошибка сервера")

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(task_id: int, task: TaskUpdate):
    """Обновление задачи."""
    updated = await update_task(
        task_id=task_id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        status=task.status
    )
    if updated:
        task_data = await get_task(task_id)
        if task_data:
            logger.info(f"API: Обновлена задача: id={task_id}")
            return task_data
        raise HTTPException(status_code=500, detail="Не удалось получить обновлённую задачу")
    logger.warning(f"API: Задача не найдена для обновления: id={task_id}")
    raise HTTPException(status_code=404, detail="Задача не найдена")

@router.delete("/{task_id}", status_code=204)
async def delete_task_endpoint(task_id: int):
    """Удаление задачи."""
    deleted = await delete_task(task_id)
    if deleted:
        logger.info(f"API: Удалена задача: id={task_id}")
        return None
    logger.warning(f"API: Задача не найдена для удаления: id={task_id}")
    raise HTTPException(status_code=404, detail="Задача не найдена")