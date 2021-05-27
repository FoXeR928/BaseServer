import uvicorn
from config import load_config
from loguru import logger
from app import app

# Инициализация концигов
cfg = load_config()


if __name__ == "__main__":
    try:
        uvicorn.run(
            app,  # Запуск app,py
            host=cfg.ip,  # Получение значений из config.py
            port=cfg.port,
        )
    # Сообщение о работе сервера
    except Exception as err:
        # Сообщение о ошибке сервера
        logger.error(f"Server not work. ERROR: {err}")
