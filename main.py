import uvicorn
from config import load_config
from loguru import logger
from app import app

cfg = load_config()


if __name__ == "__main__":
    try:
        uvicorn.run(
            app,
            host=cfg.ip,
            port=cfg.port,
        )
    except Exception as err:
        logger.error(f"Server not work. ERROR: {err}")
