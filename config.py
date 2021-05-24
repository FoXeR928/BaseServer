import configparser
from loguru import logger

logger.add("logs/info.log", format="{time} {level} {message}")
try:
    config = configparser.ConfigParser()
    config.read("config.ini")
    logger.info(f'Host: {config["host"]["ip"]} and Port {config["host"]["port"]}')
except:
    logger.error("Host and Port not take")


class Base:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port


all = Base(config["host"]["ip"], int(config["host"]["port"]))
