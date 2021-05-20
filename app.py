import fastapi
import logs
from loguru import logger

app= fastapi.FastAPI()

try:
    @app.get('/info')
    def root():
        return{'message':'Привет'}
    logger.info('Page info work')
except:
    logger.info('Page info not work')