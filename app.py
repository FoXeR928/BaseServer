from os import name
import fastapi
import logs
from loguru import logger
from config import load_config

# Добавлени параметров логов
logs.init_log()
# Инициализация fastapi
app = fastapi.FastAPI()
user = load_config()

# Запуск страницы info
@app.get("/info")
def root():
    try:
        return {"message": "Привет"}
        # Сообщение о работе страницы
        logger.info("Page info work")
    except Exception as err:
        # Сообщение о ошибке страницы
        logger.error(f"Server not work. ERROR: {err}")


@app.get("/user_get")
def get(name: str = fastapi.Query(None)):
    return name


@app.get(f"/{name}")
def name():
    try:
        return {"message": f"Привет {name}"}
        # Сообщение о работе страницы
        logger.info("Page info work")
    except Exception as err:
        # Сообщение о ошибке страницы
        logger.error(f"Server not work. ERROR: {err}")
