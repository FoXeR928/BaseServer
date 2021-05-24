import fastapi
import logs
from loguru import logger
from config import load_config

# Добавлени параметров логов
logs.init_log()
# Инициализация fastapi
app = fastapi.FastAPI()
user=load_config()
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
    
@app.get(f"/{user.name}")
def root():
    try:
        return {"message": f"Привет {user.name}"}
        # Сообщение о работе страницы
        logger.info("Page info work")
    except Exception as err:
        # Сообщение о ошибке страницы
        logger.error(f"Server not work. ERROR: {err}")