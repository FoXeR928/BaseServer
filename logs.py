from loguru import logger


def init_log():
    logger.add("logs/info.log", format="{time} {level} {message}")