import configparser
from os import name
import logs
from loguru import logger

logs.init_log()

try:
    # Получение парараметров из config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")
    # Сообщение о получение конфигов
    logger.info(f'Host: {config["host"]["ip"]} and Port: {config["host"]["port"]}')
except Exception as err:
    # Сообщение о ошибке получения конфигов
    logger.error(f"Server not work. ERROR: {err}")


def load_config():
    return Base(
        config["host"]["ip"], int(config["host"]["port"]), config["base"]["base"]
    )


class Base:
    def __init__(self, ip, port, base):
        self.ip = ip
        self.port = port
        self.base = base
