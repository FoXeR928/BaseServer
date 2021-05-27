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


class New:
    def new_init(self, name, surename, patronymic):
        self.name = name
        self.surename = surename
        self.patronymic = patronymic


@app.on_event("startup")
def start():
    logger.info("Server work")


# Запуск страницы info
@app.get("/info")
def root():
    # Сообщение о работе страницы
    logger.info("Page info work")
    message = {"message": "Привет"}
    return message


@app.post("/user_post/")
def get_user(name: str, surename: str, patronymic: str):
    try:
        result = sql.base_recording(name, surename, patronymic)
    except Exception as err:
        message = str(err)
        logger.error(f"Server not work. ERROR: {err}")
        result = fastapi.Response(content=message, status_code=500)
    return result


@app.get("/user/{surename}")
def name(surename: str):
    try:
        name = sql.base_check(surename)
    except Exception as err:
        message = str(err)
        logger.error(f"Server not work. ERROR: {err}")
        result = fastapi.Response(content=message, status_code=404)
    try:
        # Сообщение о работе страницы
        logger.info(f"Page user/{surename} work")
        for name in name:
            result = {"message": f"Привет {name[0]} {name[1]} {name[2]}"}
    except Exception as err:
        # Сообщение о ошибке страницы
        logger.error(f"Server not work. ERROR: {err}")
        message = str(err)
        result = fastapi.Response(content=message, status_code=500)
    return result


@app.on_event("shutdown")
def shutdown():
    logger.info("Server stop work")
