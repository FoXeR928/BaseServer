from loguru import logger


def init_log():
    logger.add("t.txt", format="{time} {level} {message}")


# class logs:
#     logger.add('t.txt',format='{time} {level} {message}')
