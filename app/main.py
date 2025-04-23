from fastapi import FastAPI
from app.db import create_pool, close_pool
from app.logging_config import setup_logging
from app.routes import router as tasks_router

logger = setup_logging()

app = FastAPI(title="TODO API", version="1.0.0")


app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])


@app.on_event("startup")
async def startup_event():
    logger.info("Запуск приложения")
    await create_pool()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Остановка приложения")
    await close_pool()

@app.get("/")
async def root():
    logger.info("Запрос на главную страницу")
    return {"message": "Hello World"}