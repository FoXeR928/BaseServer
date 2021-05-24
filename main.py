import uvicorn
from config import all
import logs
from loguru import logger
from config import load_config

from app import app
cfg = load_config()
try:

    if __name__ == "__main__":
        uvicorn.run(app, host=cfg.ip, port=cfg.port)
    logger.info("Server work")
except Exception as err:
    logger.error(f"Server not work. ERROR: {err}")
