import uvicorn
from loguru import logger
from app import app
from config import ip, port


if __name__ == "__main__":
    try:
        uvicorn.run(
            app,
            host=ip,
            port=port,
        )
    except Exception as err:
        logger.error(f"Server not work. ERROR: {err}")
