from logging import info
import sqlite3
import logs
from loguru import logger
import app

logs.init_log()


try:
    connect_sql= sqlite3.connect('bd.db')
    curs=connect_sql.cursor()
    logger.debug('Base connect')
except sqlite3.Error and Exception as err:
    logger.error('Base not work. ERROR: {err}')

try:
    def base_right():
        curs.execute("""INSERT INTO tabl2(name, surename, patronymic) VALUES ('iPhone X', 'Apple', 5);""")
        return curs.fetchall()
except sqlite3.Error and Exception as err:
    logger.error('Base not work. ERROR: {err}')
try:
    def base_check():
        curs.execute(""f"SELECT name, surename, patronymic from testBD WHERE surename='{app.value()}'""")
        return curs.fetchall()
    logger.info("Base date take")
except sqlite3.Error and Exception as err:
    logger.error(f"Base not work. ERROR: {err}")