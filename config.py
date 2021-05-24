import configparser
import logs
from loguru import logger

def load_config():
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        logger.info(f'Host: {config["host"]["ip"]} and Port: {config["host"]["port"]}')
    except:
        logger.error("Host and Port not take")
    return Base(config["host"]["ip"], int(config["host"]["port"]))


class Base:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port


# all = Base(config["host"]["ip"], int(config["host"]["port"]))
