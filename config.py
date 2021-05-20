import configparser
import logs
from loguru import logger

try:
    config=configparser.ConfigParser()
    config.read('config.ini')
    logger.info('Host and Port take')
except:
    logger.error('Host and Port not take')

class Base:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
    
all=Base(config["host"]["ip"], int(config["host"]["port"]))