from loguru import logger

def init_log():
    #Параметрыы вывода логов
    logger.add("logs/info.log", format="{time} {level} {message}")