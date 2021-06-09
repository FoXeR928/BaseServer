from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger
from config import base
from db_set import Base


def open_base(base):
    engine = create_engine(f"sqlite:///{base}.db")
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


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
    session = open_base(base)
    try:
        record = tabl(
            device_id=device_id,
            device_path=content,
            device_reg=regist,
            date_in=date_in,
        )
        session.add(record)
        logger.debug(f"Base recording. {device_id}")
        session.commit()
        return {"err": 0, "result": "Record created"}
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
        return {"err": 1, "result": err}


def write_to_database_issuing_flash_drive(
    tabl, device_id, date_out, fio, tabnum, department
):
    """
    Добавление в базу выданных флешек
    """
    session = open_base(base)
    try:
        check = session.query(tabl).filter(tabl.device_id == device_id).one()
        check.date_out = date_out
        check.fio = fio
        check.tabnum = tabnum
        check.department = department
        session.add(check)
        session.commit()
        logger.debug(f"Base recording. {device_id}")
        return {"err": 0, "result": "Record created"}
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
        return {"err": 1, "result": err}


def cleaning_resulting_flash_drive(tabl, device_id):
    """
    Очистка базы выданной флешки
    """
    session = open_base(base)
    try:
        check = session.query(tabl).filter(tabl.device_id == device_id).one()
        check.date_out = None
        check.fio = None
        check.tabnum = None
        check.department = None
        session.add(check)
        session.commit()
        logger.debug(f"Base clear. {device_id}")
        return {"err": 0, "result": "Record created"}
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
        return {"err": 1, "result": err}


def all_flash_drives_of_base(tabl):
    """
    Вывод всех данных из базу
    """
    try:
        session = open_base(base)
        check = session.query(tabl).all()
        return {"err": 0, "result": check}
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
        return {"err": 1, "result": err}


def search_flash_drive_based_on_id(tabl, device_id):
    """
    Вывод данных из базу на основе id
    """
    try:
        session = open_base(base)
        check = session.query(tabl).filter_by(device_id=device_id).all()
        return check_result(check)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
        return {"err": 1, "result": err}


def search_flash_drive_based_on_fio(tabl, fio):
    """
    Вывод данных из базу на основе ФИО
    """
    try:
        session = open_base(base)
        check = session.query(tabl).filter(tabl.fio.like("%" + fio + "%")).all()
        return check_result(check)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
        return {"err": 1, "result": err}


def search_flash_drive_based_on_tadnum(tabl, tabnum):
    """
    Вывод данных из базу на основе табельного номера
    """
    try:
        session = open_base(base)
        check = session.query(tabl).filter(tabl.tabnum.like("%" + tabnum + "%")).all()
        return check_result(check)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
        return {"err": 1, "result": err}


def search_decommissioned_flash_drives(tabl):
    """
    Вывод данных из базу, о списанных флешках
    """
    try:
        session = open_base(base)
        check = session.query(tabl).filter(tabl.fio == None, tabl.tabnum == None).all()
        return check_result(check)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
        return {"err": 1, "result": err}


def file_search_based_on_id(tabl, device_id):
    """
    Вывод данных из базу на основе id
    """
    try:
        session = open_base(base)
        check = (
            session.query(tabl.device_path, tabl.device_reg)
            .filter(tabl.device_id == device_id)
            .all()
        )
        return check_result(check)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
        return {"err": 1, "result": err}
