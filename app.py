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
        self.name=name
        self.surename=surename
        self.patronymic=patronymic

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
    return sql.base_recording(name, surename, patronymic)

@app.get("/user/{surename}")
def name(surename: str):
    name=sql.base_check(surename)
    for x in name:
        try:
            # Сообщение о работе страницы
            logger.info(f"Page user/{surename} work")  
            message={"message": f"Привет {x[0]} {x[1]} {x[2]}"}
            return message
        except Exception as err:
            # Сообщение о ошибке страницы
            logger.error(f"Server not work. ERROR: {err}")
            message=str(err)
            return fastapi.Response(content=message, status_code=500)

@app.on_event("shutdown")
def shutdown():
    logger.info("Server stop work")