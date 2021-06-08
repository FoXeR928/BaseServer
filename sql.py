import sqlite3
from loguru import logger
from config import base


def open_base(base):
    connect_sql = sqlite3.connect(f"{base}.db")
    curs = connect_sql.cursor()
    open_base.connect = connect_sql
    return curs


def check_result(result):
    if len(result) == 0:
        logger.debug(f"Такого нету. {result}")
        return {'err': 1, 'result':"Not result"}
    else:
        logger.debug(f"Найден. {result}")
        return {'err': 0, 'result':result}


def write_to_database_flash_drive(tabl, device_id, content, regist, date_in):
    """
    Добавления в базу Файла
    """
    curs = open_base(base)
    curs.execute(f"SELECT device_id FROM {tabl} WHERE device_id='{device_id}'")
    if len(curs.fetchall()) == 0:
        try:
            curs.execute(
                f"INSERT INTO {tabl}(device_id, device_path, device_reg, date_in) VALUES ('{device_id}', '{content}', '{regist}', '{date_in}');"
            )
            logger.debug(f"Base recording. {device_id}")
            open_base.connect.commit()
        except Exception as err:
            logger.error(f"Base recording. ERROR: {err}")
        return {'err': 0, 'result':'Record created'}
    else:
        return {'err': 1, 'result':'Has already'} 


def write_to_database_issuing_flash_drive(tabl, device_id, date_out, fio, tabnum, department):
    """
    Добавления в базу выдачи флешки
    """
    curs = open_base(base)
    curs.execute(f"SELECT device_id FROM {tabl} WHERE device_id='{device_id}'")
    if len(curs.fetchall()) != 0:
        try:
            curs.execute(
                f"UPDATE {tabl} SET date_out='{date_out}', fio= '{fio}', tabnum='{tabnum}', department='{department}' WHERE device_id='{device_id}'"
            )
            logger.debug(f"Base recording. {device_id}")
            open_base.connect.commit()
            return {'err': 0, 'result':'Record created'}
        except Exception as err:
            logger.error(f"Base recording. ERROR: {err}")
    else:
        logger.debug(f"Такого нету. {device_id}")
        return {'err': 1, 'result':"Not result"}


def cleaning_resulting_flash_drive(tabl, device_id):
    """
    Очистка базы выданной флешки
    """
    curs = open_base(base)
    curs.execute(
        f"SELECT date_out, fio, tabnum, department FROM {tabl} WHERE device_id='{device_id}'"
    )
    if len(curs.fetchall()) != 0:
        try:
            curs.execute(
                f"UPDATE {tabl} SET date_out=NULL, fio= NULL, tabnum=NULL, department=NULL WHERE device_id='{device_id}'"
            )
            logger.debug(f"Base clear. {device_id}")
            open_base.connect.commit()
            return {'err': 0, 'result':'Record created'}
        except Exception as err:
            logger.error(f"Base recording. ERROR: {err}")
    else:
        logger.debug(f"Clear or not in base. {device_id}")
        return {'err': 1, 'result':"Not result"}

def all_flash_drives_of_base(tabl):
    """
    Вывода всех данных из базу
    """
    try:
        curs = open_base(base)
        curs.execute(f"SELECT * FROM {tabl}")
        return {'err': 0, 'result':curs.fetchall()}
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")


def search_flash_drive_based_on_id(tabl, device_id):
    """
    Вывода данных на основе id из базу
    """
    try:
        curs = open_base(base)
        curs.execute(f"SELECT * FROM {tabl} WHERE device_id like '%{device_id}%'")
        result = curs.fetchall()
        return check_result(result)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")


def search_flash_drive_based_on_fio_or_tadnumder(tabl, fiotab):
    """
    Вывода данных на основе имени или таб.ном из базу
    """
    try:
        curs = open_base(base)
        curs.execute(
            f"SELECT * FROM {tabl} WHERE fio like '%{fiotab}%' OR tabnum like '%{fiotab}%'"
        )
        result = curs.fetchall()
        return check_result(result)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")


def search_decommissioned_flash_drives(tabl):
    """
    Вывода данных о списанных флешках из базу
    """
    try:
        curs = open_base(base)
        curs.execute(
            f"SELECT * FROM {tabl} WHERE date_out IS NOT NULL AND (fio IS NULL OR tabnum IS NULL)"
        )
        result = curs.fetchall()
        return check_result(result)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")


def file_search_based_on_id(tabl, device_id):
    """
    Вывода данных на основе id из базу
    """
    try:
        curs = open_base(base)
        curs.execute(
            f"SELECT device_path, device_reg FROM {tabl} WHERE device_id='{device_id}'"
        )
        result = curs.fetchall()
        return check_result(result)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
