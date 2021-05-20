from logs import logs
import uvicorn
from config import all
import logs
from loguru import logger

try:
    if __name__=='__main__':
        uvicorn.run(
            'app:app',
            host=all.ip,
            port=all.port,
            reload=True)
    logger.info('Server work')
except:
    logger.error('Server not work')