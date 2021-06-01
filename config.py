import configparser
import os
from loguru import logger

if "config.txt" not in os.listdir():
    conf = open("config.txt", "w+")
    if os.stat("config.txt").st_size == 0:
        while True:
            file = input("Введите имя файла с конфигурациями: ")
            if file in os.listdir():
                conf.write(file)
                conf.close()
                break
            else:
                print("Введён не верный файл")
else:
    pass
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
