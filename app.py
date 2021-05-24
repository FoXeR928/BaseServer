import fastapi
from loguru import logger

logger.add("logs/info.log", format="{time} {level} {message}")
app = fastapi.FastAPI()

try:

    @app.get("/info")
    def root():
        return {"message": "Привет"}

    logger.info("Page info work")
except:
    logger.info("Page info not work")
