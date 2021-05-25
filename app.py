import fastapi
import logs
from loguru import logger
from config import load_config

# Добавлени параметров логов
logs.init_log()
# Инициализация fastapi
app = fastapi.FastAPI()
user = load_config()

@app.on_event("startup")
def start():
    logger.info("Server work")

# Запуск страницы info
@app.get("/info")
def root():
    try:
        # Сообщение о работе страницы
        logger.info("Page info work")
        message={"message": "Привет"}
        return message
    except Exception as err:
        # Сообщение о ошибке страницы
        logger.error(f"Server not work. ERROR: {err}")
        message=str(err)
        return fastapi.Response(content=message)

@app.get("/user_get/")
def get(name: str = fastapi.Query(None)):
    return name


@app.get("/user/{name}")
def name(name: str):
    try:
        # Сообщение о работе страницы
        logger.info(f"Page user/{name} work")   
        message={"message": f"Привет {10/0}"}
        return message
    except Exception as err:
        # Сообщение о ошибке страницы
        logger.error(f"Server not work. ERROR: {err}")
        message=str(err)
        return fastapi.Response(content=message)

@app.on_event("shutdown")
def shutdown():
    logger.info("Server stop work")