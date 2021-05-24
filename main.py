import uvicorn
from config import load_config

from loguru import logger
from app import app

cfg = load_config()

try:
    if __name__ == "__main__":
        uvicorn.run(app, host=cfg.ip, port=cfg.port)
        # uvicorn.run("app:app", host=cfg.ip, port=cfg.port, reload=True)
    logger.info("Server work")
except Exception as err:
    logger.error(f"Server not work. ERROR: {err}")
