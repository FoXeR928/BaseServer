import sqlite3
from loguru import logger
from config import load_config

cfg = load_config()

# Функция добавления в базу Файла
def base_recording_file(device_id, content, regist, date_in):
    connect_sql = sqlite3.connect("bd.db", timeout=5)
    curs = connect_sql.cursor()
    curs.execute(f"SELECT device_id FROM {cfg.tabl_file} WHERE device_id='{device_id}'")
    if len(curs.fetchall()) == 0:
        try:
            curs.execute(
                f"INSERT INTO {cfg.tabl_file}(device_id, device_path, device_reg, date_in) VALUES ('{device_id}', '{content}', '{regist}', '{date_in}');"
            )
            logger.debug(f"Base recording. {device_id}")
            connect_sql.commit()
        except Exception as err:
            logger.error(f"Base recording. ERROR: {err}")
        return "Файл добавлен в базу"
    else:
        return "Уже есть в базе"


# Функция добавления в базу выдачи флешки
def base_recording_file_device(device_id, date_out, fio, tabnum, department):
    connect_sql = sqlite3.connect("bd.db", timeout=5)
    curs = connect_sql.cursor()
    curs.execute(f"SELECT device_id FROM {cfg.tabl_file} WHERE device_id='{device_id}'")
    if len(curs.fetchall()) != 0:
        try:
            curs.execute(
                f"UPDATE {cfg.tabl_file} SET date_out='{date_out}', fio= '{fio}', tabnum='{tabnum}', department='{department}' WHERE device_id='{device_id}'"
            )
            connect_sql.commit()
        except Exception as err:
            logger.error(f"Base recording. ERROR: {err}")
    else:
        return "Такого нет в базе"


# Функция очистки базу выданной флешки
def base_clear_device(device_id):
    connect_sql = sqlite3.connect("bd.db", timeout=5)
    curs = connect_sql.cursor()
    curs.execute(
        f"SELECT date_out, fio, tabnum, department FROM {cfg.tabl_file} WHERE device_id='{device_id}'"
    )
    if len(curs.fetchall()) != 0:
        try:
            curs.execute(
                f"UPDATE {cfg.tabl_file} SET date_out=NULL, fio= NULL, tabnum=NULL, department=NULL WHERE device_id='{device_id}'"
            )
            connect_sql.commit()
        except Exception as err:
            logger.error(f"Base recording. ERROR: {err}")
    else:
        return "Данных и так нет"


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
        if len(curs.fetchall()) == 0:
            return "Такой в базе нету"
        else:
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
        if len(curs.fetchall()) == 0:
            return "Такого в базе нету"
        else:
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
        if len(curs.fetchall()) == 0:
            return "Такого в базе нету"
        else:
            return curs.fetchall()
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
