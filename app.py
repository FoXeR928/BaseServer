import fastapi
from loguru import logger

# Путь записи логов
logger.add("logs/info.log", format="{time} {level} {message}")
# Инициализация fastapi
app = fastapi.FastAPI()

try:
    # Создание страницы
    @app.get("/info")
    def root():
        return {"message": "Привет"}

    logger.info("Page info work")
except:
    logger.info("Page info not work")
