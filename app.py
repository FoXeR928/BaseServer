import fastapi
import logs
from loguru import logger
from config import load_config
import sql

# Добавлени параметров логов
logs.init_log()
# Инициализация fastapi
app = fastapi.FastAPI()
user = load_config()

def value(surename):
    print (surename)

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
        return fastapi.Response(content=message, status_code=500)


@app.get("/user_get/")
def get_user(name: str, surename: str, patronymic: str):
    return name, surename, patronymic

@app.get("/user/{surename}")
def name(surename: str):
    value(surename)
    name=sql.base_check()
    try:
        # Сообщение о работе страницы
        logger.info(f"Page user/{surename} work")  
        message={"message": f"Привет {name}"}
        return message
    except Exception as err:
        # Сообщение о ошибке страницы
        logger.error(f"Server not work. ERROR: {err}")
        message=str(err)
        return fastapi.Response(content=message, status_code=500)

@app.on_event("shutdown")
def shutdown():
    logger.info("Server stop work")
