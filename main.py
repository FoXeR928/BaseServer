import uvicorn
from loguru import logger
import logs
import sys
import os

if "config.txt" not in os.listdir() or os.stat("config.txt").st_size == 0:
    file, file_name = sys.argv
    conf = open("config.txt", "w+")
    conf.write(file_name)
    conf.close()

logs.init_log()
from config import load_config, take_host
from app import app

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
