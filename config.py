import configparser
from loguru import logger

# Путь записи логов
logger.add("logs/info.log", format="{time} {level} {message}")
try:
    # Инициализация configparser
    config = configparser.ConfigParser()
    # Получение данных из config.init
    config.read("config.ini")
    logger.info(f'Host: {config["host"]["ip"]} and Port {config["host"]["port"]}')
except:
    logger.error("Host and Port not take")

# Класс получения тегов
class Base:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port


# Введение переменных в класс
all = Base(config["host"]["ip"], int(config["host"]["port"]))
