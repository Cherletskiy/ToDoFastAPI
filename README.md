# TODO API

REST API для управления задачами (To-Do List), построенное с использованием **FastAPI** и **PostgreSQL**. API поддерживает CRUD-операции (создание, чтение, обновление, удаление задач), фильтрацию по статусу и логирование всех действий.

## Основные возможности

- Создание, просмотр, обновление и удаление задач.
- Фильтрация задач по статусу (`pending`, `completed`).
- Логирование всех операций в файл (`logs/app.log`).
- Интерактивная документация API через Swagger (`/docs`).

## Технологии

- **FastAPI**
- **PostgreSQL**
- **Docker & Docker Compose**
- **Pydantic**
- **Asyncpg**
- **Python 3.12**

## Требования

- **Docker** (версия 20.10 или выше).
- **Docker Compose** (версия 2.x, плагин для Docker CLI).
- **Git** (для клонирования репозитория, опционально).

## Установка

1. **Клонируйте репозиторий**:
   ```bash
   git clone <ваш-репозиторий>
   cd ToDoFastAPI
   ```

2. **Убедитесь, что Docker и Docker Compose установлены**:
   ```bash
   docker --version
   docker compose version
   ```
   Если Docker Compose не установлен, выполните:
   ```bash
   sudo apt update
   sudo apt install docker-compose-plugin
   ```

3. **Создайте директорию для логов**:
   ```bash
   mkdir -p logs
   chmod -R u+rw logs
   ```

## Переменные окружения

Файл `.env` содержит настройки для подключения к базе данных:

```plaintext
DB_HOST=postgres
DB_PORT=5432
DB_NAME=todo
DB_USER=postgres
DB_PASSWORD=postgres
```

## Запуск

Проект разворачивается одной командой с помощью Docker Compose:

```bash
docker compose up --build
```

### Доступ к API:
- Откройте в браузере: `http://localhost:8000/docs` (Swagger UI).
- Используйте `http://localhost:8000/redoc` для альтернативной документации.


## Тестирование API

API предоставляет следующие эндпоинты (доступны через Swagger):

1. **Создать задачу**:
   - `POST /tasks`
   - Тело запроса:
     ```json
     {
       "title": "Купить продукты",
       "description": "Молоко, хлеб, яйца",
       "due_date": "2025-12-31T23:59:59",
       "status": "pending"
     }
     ```

2. **Получить список задач**:
   - `GET /tasks`
   - Фильтры (опционально): `?status=pending` или `?status=completed`.

3. **Получить задачу по ID**:
   - `GET /tasks/{task_id}`

4. **Обновить задачу**:
   - `PUT /tasks/{task_id}`
   - Тело запроса (поля опциональны):
     ```json
     {
       "title": "Обновлённая задача",
       "status": "completed"
     }
     ```

5. **Удалить задачу**:
   - `DELETE /tasks/{task_id}`

## Структура проекта

```
ToDoFastAPI/
├── app/
│   ├── __init__.py
│   ├── crud.py         # Логика CRUD-операций
│   ├── db.py           # Подключение к PostgreSQL
│   ├── logging_config.py # Настройка логирования
│   ├── main.py         # Главный файл FastAPI
│   ├── routes.py       # Маршруты API
│   ├── schemas.py      # Pydantic-модели с валидацией
├── logs/
│   ├── app.log         # Логи приложения
├── .env                # Переменные окружения
├── Dockerfile          # Конфигурация образа FastAPI
├── docker-compose.yml  # Конфигурация Docker Compose
├── init.sql            # Инициализация таблицы tasks
├── requirements.txt    # Зависимости Python
├── README.md           # Документация
```



