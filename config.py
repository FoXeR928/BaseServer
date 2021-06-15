import configparser
import os
import logs
from loguru import logger

logs.init_log()

# Функция поиска параметров в конфигах
def load_config():
    try:
        config = configparser.ConfigParser()
        config.read(os.environ["Config"])
        logger.info(f'Host: {config["host"]["ip"]} and Port: {config["host"]["port"]}')
    except Exception as err:
        logger.error(f"Server not work. ERROR: {err}")
    try:
        result = Base(
            config["host"]["ip"],
            int(config["host"]["port"]),
            config["base"]["base"],
            config["tabl"]["tabl_file"],
        )
    except Exception as err:
        logger.error(f"Server not work. ERROR: {err}")
    return result


# Класс вывода конфигов
class Base:
    def __init__(self, ip, port, base, tabl_file):
        self.ip = ip
        self.port = port
        self.base = base
        self.tabl_file = tabl_file


cfg = load_config()
base = cfg.base
tabl_name = cfg.tabl_file
ip = cfg.ip
port = cfg.port

from db_set import Tabl

tabl = Tabl
