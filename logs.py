from loguru import logger

class logs:
    logger.add('t.txt',format='{time} {level} {message}')