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
def base_recording_file(device_id, content, regist, date_in):
    try:
        connect_sql = sqlite3.connect("bd.db", timeout=5)
        curs = connect_sql.cursor()
        curs.execute(
            f"INSERT INTO {cfg.tabl_file}(device_id, device_path, device_reg, date_in) VALUES ('{device_id}', '{content}', '{regist}', '{date_in}');"
        )
        logger.debug(f"Base recording. {device_id}")
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
    connect_sql.commit()


# Функция добавления в базу выдачи флешки
def base_recording_file_device(device_id, date_out, fio, tabnum, department):
    try:
        connect_sql = sqlite3.connect("bd.db", timeout=5)
        curs = connect_sql.cursor()
        curs.execute(
            f"UPDATE {cfg.tabl_file} SET date_out='{date_out}', fio= '{fio}', tabnum='{tabnum}', department='{department}' WHERE device_id='{device_id}'"
        )
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
    connect_sql.commit()


# Функция очистки базу выданной флешки
def base_clear_device(device_id):
    try:
        connect_sql = sqlite3.connect("bd.db", timeout=5)
        curs = connect_sql.cursor()
        curs.execute(
            f"UPDATE {cfg.tabl_file} SET date_out=NULL, fio= NULL, tabnum=NULL, department=NULL WHERE device_id='{device_id}'"
        )
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
    connect_sql.commit()


# Функция вывода всех данных из базу
def base_all_flask():
    try:
        connect_sql = sqlite3.connect("bd.db", timeout=5)
        curs = connect_sql.cursor()
        curs.execute(f"SELECT * FROM {cfg.tabl_file}")
        return curs.fetchall()
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")


# Функция вывода данных на основе id из базу
def base_check_flask_id(device_id):
    try:
        connect_sql = sqlite3.connect("bd.db", timeout=5)
        curs = connect_sql.cursor()
        curs.execute(
            f"SELECT * FROM {cfg.tabl_file} WHERE device_id like '%{device_id}%'"
        )
        return curs.fetchall()
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")


# Функция вывода данных на основе имени или таб.ном из базу
def base_check_flask_name(fiotab):
    try:
        connect_sql = sqlite3.connect("bd.db", timeout=5)
        curs = connect_sql.cursor()
        curs.execute(
            f"SELECT * FROM {cfg.tabl_file} WHERE fio like '%{fiotab}%' OR tabnum like '%{fiotab}%'"
        )
        return curs.fetchall()
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")


# Функция вывода данных о списанных флешках из базу
def base_check_flask_off():
    try:
        connect_sql = sqlite3.connect("bd.db", timeout=5)
        curs = connect_sql.cursor()
        curs.execute(
            f"SELECT * FROM {cfg.tabl_file} WHERE date_out IS NOT NULL AND (fio OR tabnum IS NULL)"
        )
        return curs.fetchall()
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")


# Функция вывода данных на основе id из базу
def base_date_flask(device_id):
    try:
        connect_sql = sqlite3.connect("bd.db", timeout=5)
        curs = connect_sql.cursor()
        curs.execute(
            f"SELECT device_path, device_reg FROM {cfg.tabl_file} WHERE device_id='{device_id}'"
        )
        return curs.fetchall()
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")


# Функция поиска в базе
def base_check(surename):
    try:
        connect_sql = sqlite3.connect("bd.db", timeout=5)
        curs = connect_sql.cursor()
        curs.execute(
            f"SELECT name, surename, patronymic from {cfg.tabl_tb} WHERE surename='{surename}'"
        )
        logger.info("Base date take")
        return curs.fetchall()
    except Exception as err:
        logger.error(f"Base not take. ERROR: {err}")
