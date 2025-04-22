import logging
from logging.handlers import RotatingFileHandler
from typing import Optional
import json
import os


def setup_logging(
    log_file: str = 'logs/app.log',
    max_bytes: int = 1024 * 1024,
    backup_count: int = 5,
    log_level: str = 'INFO',
    config_file: Optional[str] = None,
    use_console: bool = True
) -> logging.Logger:
    logger = logging.getLogger('todo_app')
    try:
        logger.setLevel(getattr(logging, log_level.upper()))
    except AttributeError:
        logger.error(f"Недопустимый уровень логирования: {log_level}. Используется INFO.")
        logger.setLevel(logging.INFO)

    # Временный хендлер для ошибок конфигурации
    temp_handler = logging.StreamHandler()
    temp_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(temp_handler)

    # Загрузка конфигурации
    if config_file and os.path.exists(config_file):
        try:
            with open(config_file) as f:
                config = json.load(f)
            log_file = config.get('log_file', log_file)
            max_bytes = config.get('max_bytes', max_bytes)
            backup_count = config.get('backup_count', backup_count)
            log_level = config.get('log_level', log_level)
            logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка чтения конфигурационного файла {config_file}: {e}")
        except Exception as e:
            logger.error(f"Непредвиденная ошибка при чтении {config_file}: {e}")

    # Основные хендлеры
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s'
    )
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    # Очищаем хендлеры
    if logger.hasHandlers():
        logger.handlers.clear()

    # Добавляем хендлеры
    logger.addHandler(file_handler)
    if use_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(log_level)
        logger.addHandler(console_handler)

    return logger

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger('todo_app.' + name)