import configparser
from loguru import logger

# Путь записи логов
logger.add("logs/info.log", format="{time} {level} {message}")
def load_config():
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        logger.info(f'Host: {config["host"]["ip"]} and Port: {config["host"]["port"]}')
    except:
        logger.error("Host and Port not take")
    return Base(config["host"]["ip"], int(config["host"]["port"]))

# Класс получения тегов
class Base:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

