import sqlite3
from loguru import logger
from config import load_config

cfg = load_config()

# Функция добавления в базу ФИО
def base_recording(name, surename, patronymic):
    try:
        connect_sql = sqlite3.connect(f"{cfg.base}.db", timeout=5)
        curs = connect_sql.cursor()
        curs.execute(
            f"INSERT INTO {cfg.tabl_tb}(name, surename, patronymic) VALUES ('{name}', '{surename}', '{patronymic}');"
        )
        logger.debug(f"Base recording. {name, surename, patronymic}")
        connect_sql.commit()
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")


# Функция добавления в базу Файла
def base_recording_file(name, content):
    try:
        connect_sql = sqlite3.connect("bd.db", timeout=5)
        curs = connect_sql.cursor()
        curs.execute(
            f"INSERT INTO {cfg.tabl_file}(name, content) VALUES ('{name}', '{content}');"
        )
        logger.debug(f"Base recording. {name}")
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
    connect_sql.commit()


# Функция поиска в базе
def base_check(surename):
    try:
        connect_sql = sqlite3.connect("bd.db", timeout=5)
        curs = connect_sql.cursor()
        curs.execute(
            f"SELECT name, surename, patronymic from {cfg.tabl_tb} WHERE surename='{surename}'"
        )
        logger.info("Base date take")
    except Exception as err:
        logger.error(f"Base not take. ERROR: {err}")
    return curs.fetchall()
