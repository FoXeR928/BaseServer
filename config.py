import configparser
import os
from loguru import logger


while True:
    file=input('Введите имя файла с конфигурациями: ')
    if file in os.listdir():
        # Чтение конфигов
        def take_host():
            try:
                config = configparser.ConfigParser()
                config.read(f"{file}")
                logger.info(f'Host: {config["host"]["ip"]} and Port: {config["host"]["port"]}')
            except Exception as err:
                logger.error(f"Server not work. ERROR: {err}")


        # Функция поиска параметров в конфигах
        def load_config():
            try:
                config = configparser.ConfigParser()
                config.read("config.ini")
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
        break
    else:
        print('Введён не верный файл')