import fastapi
import logs
from loguru import logger

#Добавлени параметров логов
logs.init_log()
#Инициализация fastapi
app = fastapi.FastAPI()

try:

    #Запуск страницы info
    @app.get("/info")
    def root():
        return {"message": "Привет"}

    #Сообщение о работе страницы
    logger.info("Page info work")
except Exception as err:
    #Сообщение о ошибке страницы
    logger.error(f"Server not work. ERROR: {err}")
