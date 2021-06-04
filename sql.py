import sqlite3
from loguru import logger
from config import load_config

cfg = load_config()


def open_base():
    connect_sql = sqlite3.connect(f"{cfg.base}.db", timeout=5)
    curs = connect_sql.cursor()
    connect_sql.commit()
    return curs

def check_result(result):
    if len(result) == 0:
        logger.debug(f"Такого нету. {result}")
        return "Такого в базе нету"
    else:
        logger.debug(f"Найден. {result}")
        return result

# Функция добавления в базу Файла
def write_to_database_flash_drive (device_id, content, regist, date_in):
    curs=open_base()
    curs.execute(f"SELECT device_id FROM {cfg.tabl_file} WHERE device_id='{device_id}'")
    if len(curs.fetchall()) == 0:
        try:
            curs.execute(
                f"INSERT INTO {cfg.tabl_file}(device_id, device_path, device_reg, date_in) VALUES ('{device_id}', '{content}', '{regist}', '{date_in}');"
            )
            logger.debug(f"Base recording. {device_id}")
        except Exception as err:
            logger.error(f"Base recording. ERROR: {err}")
        return "Файл добавлен в базу"
    else:
        return "Уже есть в базе"


# Функция добавления в базу выдачи флешки
def write_to_database_issuing_flash_drive(device_id, date_out, fio, tabnum, department):
    curs=open_base()
    curs.execute(f"SELECT device_id FROM {cfg.tabl_file} WHERE device_id='{device_id}'")
    if len(curs.fetchall()) != 0:
        try:
            curs.execute(
                f"UPDATE {cfg.tabl_file} SET date_out='{date_out}', fio= '{fio}', tabnum='{tabnum}', department='{department}' WHERE device_id='{device_id}'"
            )
            logger.debug(f"Base recording. {device_id}")
            return "Флешка выдана"
        except Exception as err:
            logger.error(f"Base recording. ERROR: {err}")
    else:
        logger.debug(f"Такого нету. {device_id}")
        return "Такого нет в базе"


# Функция очистки базу выданной флешки
def cleaning_resulting_flash_drive(device_id):
    curs=open_base()
    curs.execute(
        f"SELECT date_out, fio, tabnum, department FROM {cfg.tabl_file} WHERE device_id='{device_id}'"
    )
    if len(curs.fetchall()) != 0:
        try:
            curs.execute(
                f"UPDATE {cfg.tabl_file} SET date_out=NULL, fio= NULL, tabnum=NULL, department=NULL WHERE device_id='{device_id}'"
            )
            logger.debug(f"Base clear. {device_id}")
            return "Флешка очищена"
        except Exception as err:
            logger.error(f"Base recording. ERROR: {err}")
    else:
        logger.debug(f"Clear or not in base. {device_id}")
        return "Данных и так нет"


# Функция вывода всех данных из базу
def all_flash_drives_of_base():
    try:
        curs=open_base()
        curs.execute(f"SELECT * FROM {cfg.tabl_file}")
        return curs.fetchall()
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")


# Функция вывода данных на основе id из базу
def search_flash_drive_based_on_id(device_id):
    try:
        curs=open_base()
        curs.execute(
            f"SELECT * FROM {cfg.tabl_file} WHERE device_id like '%{device_id}%'"
        )
        result = curs.fetchall()
        return check_result(result)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")


# Функция вывода данных на основе имени или таб.ном из базу
def search_flash_drive_based_on_fio_or_tadnumder(fiotab):
    try:
        curs=open_base()
        curs.execute(
            f"SELECT * FROM {cfg.tabl_file} WHERE fio like '%{fiotab}%' OR tabnum like '%{fiotab}%'"
        )
        result = curs.fetchall()
        return check_result(result)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")


# Функция вывода данных о списанных флешках из базу
def search_decommissioned_flash_drives():
    try:
        curs=open_base()
        curs.execute(
            f"SELECT * FROM {cfg.tabl_file} WHERE date_out IS NOT NULL AND (fio IS NULL OR tabnum IS NULL)"
        )
        result = curs.fetchall()
        return check_result(result)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")


# Функция вывода данных на основе id из базу
def file_search_based_on_id(device_id):
    try:
        curs=open_base()
        curs.execute(
            f"SELECT device_path, device_reg FROM {cfg.tabl_file} WHERE device_id='{device_id}'"
        )
        result = curs.fetchall()
        return check_result(result)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
