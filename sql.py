from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_set import base, tabl
from loguru import logger


def open_base():
    engine = create_engine('sqlite:///flask-date.db')
    base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


def check_result(result):
    if len(result) == 0:
        logger.debug(f"Not found {result}")
        return [404, "Not found"]
    else:
        logger.debug(f"Found. {result}")
        return [[200, 'Status ok'], result]


def write_to_database_flash_drive(device_id, content, regist, date_in):
    """
    Функция добавления в базу Файла
    """
    session = open_base()
    check=session.query(tabl).filter(tabl.device_id==device_id).count()
    if check == 0:
        try:
            record=tabl(device_id=device_id, device_path=content, device_reg=regist, date_in=date_in)
            session.add(record)
            session.commit()
            logger.debug(f"Base recording. {device_id}")
        except Exception as err:
            logger.error(f"Base recording. ERROR: {err}")
        return [201, 'record created']
    else:
        return [208, 'Not all values ​​were transferred']


def write_to_database_issuing_flash_drive(device_id, date_out, fio, tabnum, department):
    """
    Функция добавления в базу выдачи флешки
    """
    session = open_base()
    check=session.query(tabl).filter(tabl.device_id==device_id).one()
    check_if=session.query(tabl).filter(tabl.device_id==device_id).count()
    if check_if>0:
        try:
            check.date_out=date_out
            check.fio=fio
            check.tabnum=tabnum
            check.department=department
            session.add(check)
            session.commit()
            logger.debug(f"Base recording. {device_id}")
            return [201, 'record created']
        except Exception as err:
            logger.error(f"Base recording. ERROR: {err}")
    else:
        logger.debug(f"Not found. {device_id}")
        return [404, "Not result"]


def cleaning_resulting_flash_drive(device_id):
    """
    Функция очистки базу выданной флешки
    """
    session = open_base()
    check=session.query(tabl).filter(tabl.device_id==device_id).one()
    check_if=session.query(tabl).filter(tabl.device_id==device_id).count()
    if check_if>0:
        try:
            check.date_out=None
            check.fio=None
            check.tabnum=None
            check.department=None
            session.add(check)
            session.commit()
            logger.debug(f"Base clear. {device_id}")
            return [201, 'record created']
        except Exception as err:
            logger.error(f"Base recording. ERROR: {err}")
    else:
        logger.debug(f"Clear or not in base. {device_id}")
        return [404, "Not result"]


def all_flash_drives_of_base():
    """
    Функция вывода всех данных из базу
    """
    try:
        session = open_base()
        check=session.query(tabl).all()
        return ([200, 'Status ok'], check)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")


def search_flash_drive_based_on_id(device_id):
    """
    Функция вывода данных на основе id из базу
    """
    try:
        session = open_base()
        check=session.query(tabl).filter_by(device_id=device_id).all()
        return check_result(check)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")


def search_flash_drive_based_on_fio_or_tadnumder(fiotab):
    """
    Функция вывода данных на основе имени или таб.ном из базу
    """
    try:
        session = open_base()
        check=session.query(tabl).filter(tabl.fio==fiotab or tabl.tabnum==fiotab).all()
        return check_result(check)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")


def search_decommissioned_flash_drives():
    """
    Функция вывода данных о списанных флешках из базу
    """
    try:
        session = open_base()
        check=session.query(tabl).filter(tabl.fio==None and tabl.tabnum==None).all()
        return check_result(check)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")


def file_search_based_on_id(device_id):
    """
    Функция вывода данных на основе id из базу
    """
    try:
        session = open_base()
        check=session.query(tabl.device_path, tabl.device_reg).filter(tabl.device_id==device_id).all()
        return check_result(check)
    except Exception as err:
        logger.error(f"Base recording. ERROR: {err}")
