import configparser
import os
import sys
from loguru import logger


if "config.txt" not in os.listdir() or os.stat("config.txt").st_size == 0:
    file, file_name = sys.argv
    conf = open("config.txt", "w+")
    conf.write(file_name)
    conf.close()
config_file = open("config.txt", "r").read()
config = configparser.ConfigParser()
config.read(f"{config_file}")
# Чтение конфигов
def take_host():
    try:
        logger.info(f'Host: {config["host"]["ip"]} and Port: {config["host"]["port"]}')
    except Exception as err:
        logger.error(f"Server not work. ERROR: {err}")


# Функция поиска параметров в конфигах
def load_config():
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
