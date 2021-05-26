from logging import info
from os import name
import sqlite3
import logs
from loguru import logger

logs.init_log()

try:
    connect_sql= sqlite3.connect('bd.db')
    curs=connect_sql.cursor()
    logger.debug('Base connect')
except:
    logger.error('Base not connect')

try:
    def base_check():
        curs.execute("""SELECT id_name, name from testBD""")
        return(curs.fetchall())
    logger.info("Base date take")
except sqlite3.Error and Exception as err:
    logger.error(f"Base not work. ERROR: {err}")