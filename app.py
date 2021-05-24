import fastapi
import logs
from loguru import logger

logs.init_log()
app = fastapi.FastAPI()

try:

    @app.get("/info")
    def root():
        logger.debug("Page info work")
        return {"message": "Привет"}

    logger.info("Page info work")
except:
    logger.info("Page info not work")


