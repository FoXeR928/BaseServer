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
        return {"err": 1, "result": "Not result"}
    else:
        logger.debug(f"Найден. {result}")
        return {"err": 0, "result": result}


def write_to_database_flash_drive(tabl, device_id, content, regist, date_in):
    """
    Добавление в базу Файла и id
    """
    curs = open_base(base)
    try:
        curs.execute(
            f"INSERT INTO {tabl}(device_id, device_path, device_reg, date_in) VALUES ('{device_id}', '{content}', '{regist}', '{date_in}');"
        )
        logger.debug(f"Base recording. {device_id}")
        open_base.connect.commit()
        return {"err": 0, "result": "Record created"}
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
        open_base.connect.commit()
        return {"err": 1, "result": err}


def write_to_database_issuing_flash_drive(
    tabl, device_id, date_out, fio, tabnum, department
):
    """
    Добавление в базу выданных флешек
    """
    curs = open_base(base)
    curs.execute(f"SELECT device_id FROM {tabl} WHERE device_id='{device_id}'")
    if len(curs.fetchall())>0:
        try:
            curs.execute(
                f"UPDATE {tabl} SET date_out='{date_out}', fio= '{fio}', tabnum='{tabnum}', department='{department}' WHERE device_id='{device_id}'"
            )
            logger.debug(f"Base recording. {device_id}")
            open_base.connect.commit()
            return {"err": 0, "result": "Record created"}
        except Exception as err:
            logger.error(f"Base recording. ERROR: {err}")
            return {"err": 1, "result": err}
    else:
        return {"err": 1, "result": 'Уже ессть в базе'}
    


def cleaning_resulting_flash_drive(tabl, device_id):
    """
    Очистка базы выданной флешки
    """
    curs = open_base(base)
    curs.execute(f"SELECT device_id FROM {tabl} WHERE device_id='{device_id}'")
    if len(curs.fetchall())>0:
        try:
            curs.execute(
                f"UPDATE {tabl} SET date_out=NULL, fio= NULL, tabnum=NULL, department=NULL WHERE device_id='{device_id}'"
            )
            logger.debug(f"Base clear. {device_id}")
            open_base.connect.commit()
            return {"err": 0, "result": "Record created"}
        except Exception as err:
            logger.error(f"Base recording. ERROR: {err}")
            return {"err": 1, "result": err}
    else:
        return {"err": 1, "result": 'Уже ессть в базе'}


def all_flash_drives_of_base(tabl):
    """
    Вывод всех данных из базу
    """
    try:
        curs = open_base(base)
        curs.execute(f"SELECT * FROM {tabl}")
        return {"err": 0, "result": curs.fetchall()}
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
        return {"err": 1, "result": err}


def search_flash_drive_based_on_id(tabl, device_id):
    """
    Вывод данных из базу на основе id
    """
    try:
        curs = open_base(base)
        curs.execute(f"SELECT * FROM {tabl} WHERE device_id like '%{device_id}%'")
        result = curs.fetchall()
        return check_result(result)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
        return {"err": 1, "result": err}


def search_flash_drive_based_on_fio(tabl, fio):
    """
    Вывод данных из базу на основе ФИО
    """
    try:
        curs = open_base(base)
        curs.execute(f"SELECT * FROM {tabl} WHERE fio like '%{fio}%'")
        result = curs.fetchall()
        return check_result(result)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
        return {"err": 1, "result": err}


def search_flash_drive_based_on_tadnum(tabl, tabnum):
    """
    Вывод данных из базу на основе табельного номера
    """
    try:
        curs = open_base(base)
        curs.execute(f"SELECT * FROM {tabl} WHERE tabnum like '%{tabnum}%'")
        result = curs.fetchall()
        return check_result(result)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
        return {"err": 1, "result": err}


def search_decommissioned_flash_drives(tabl):
    """
    Вывод данных из базу, о списанных флешках
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
        return {"err": 1, "result": err}


def file_search_based_on_id(tabl, device_id):
    """
    Вывод данных из базу на основе id
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
        return {"err": 1, "result": err}
