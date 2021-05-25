from os import name
import fastapi
from fastapi import responses
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


@app.get("/user/{name}", status_code=200)
def name(name: str, response=fastapi.Response):
    try:
        if name not in name:
            return {"Страницы нет"}
            response.status_cod=fastapi.status.HTTP_404_NOT_FOUND
        else:    
            return {"message": f"Привет {name}"}
        # Сообщение о работе страницы
        logger.info("Page info work")
    except Exception as err:
        # Сообщение о ошибке страницы
        logger.error(f"Server not work. ERROR: {err}")