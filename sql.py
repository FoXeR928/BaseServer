import sqlite3
import logs
from loguru import logger

logs.init_log()

def base_recording(name, surename, patronymic):
    try:
        connect_sql= sqlite3.connect('bd.db')
        curs=connect_sql.cursor()
        curs.execute(f"INSERT INTO testBD(name, surename, patronymic) VALUES ('{name}', '{surename}', '{patronymic}');")
        logger.debug(f'Base recording. {name, surename, patronymic}')
    except sqlite3.Error and Exception as err:
        logger.error(f'Base recording. ERROR: {err}')
    connect_sql.commit()

def base_check(surename):
    try:
        connect_sql= sqlite3.connect('bd.db', timeout=5)
        curs=connect_sql.cursor()
        curs.execute(f"SELECT name, surename, patronymic from testBD WHERE surename='{surename}'")
        logger.info("Base date take")
        
        return curs.fetchall()
    except sqlite3.Error and Exception as err:
        logger.error(f"Base not take. ERROR: {err}")