import configparser

config=configparser.ConfigParser()
config.read('config.ini')

class Base:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
    
all=Base(config["host"]["ip"], int(config["host"]["port"]))