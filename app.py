import fastapi
import logs
import sql
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
        return fastapi.Response(content=message, status_code=500)


@app.get("/user_get/")
def get(name: str = fastapi.Query(None)):
    return name
  
for x in sql.base_check():

    @app.get(f"/user/{x[0]}")
    def name():
        try:
            # Сообщение о работе страницы
            logger.info(f"Page user/{x[0]} work")  
            message={"message": f"Привет {x[1]}"}
            return message
        except Exception as err:
            # Сообщение о ошибке страницы
            logger.error(f"Server not work. ERROR: {err}")
            message=str(err)
            return fastapi.Response(content=message, status_code=500)

    @app.on_event("shutdown")
    def shutdown():
        logger.info("Server stop work")