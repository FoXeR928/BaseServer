import uvicorn
from config import load_config, take_host
from loguru import logger
import logs
from app import app

logs.init_log()
take_host()
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
