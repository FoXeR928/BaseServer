import fastapi
import logs
from loguru import logger
from config import load_config
import sql
import datetime

logs.init_log()
app = fastapi.FastAPI()
user = load_config()


@app.on_event("startup")
def start():
    logger.info("Server work")


@app.get("/info")
def root():
    """
    Приветствующая страница
    """
    logger.debug("Page info work")
    message = {"message": "Привет"}
    return message


@app.post("/user_post/", status_code=fastapi.status.HTTP_201_CREATED)
def post_user(name: str, surename: str, patronymic: str, code: fastapi.Response):
    """
    Добавление в базу ФИО
    """
    try:
        message = sql.base_recording(name, surename, patronymic)
    except Exception as err:
        message = str(err)
        logger.error(f"Server not work. ERROR: {err}")
        code.status_code = fastapi.status.HTTP_501_NOT_IMPLEMENTED
    return message


@app.get("/user/{surename}", status_code=fastapi.status.HTTP_200_OK)
def name(surename: str, code: fastapi.Response):
    """
    Вывод из базы приветствия на основе фамилии
    """
    message = {"Ошибка": "Ничего не найдено"}
    try:
        name = sql.base_check(surename)
        for name in name:
            message = {"message": f"Привет {name[0]} {name[1]} {name[2]}"}
        logger.debug(f"Page user/{surename} work")
    except Exception as err:
        logger.error(f"Server not work. ERROR: {err}")
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        message = {"Error": f"{str(err)}"}
    return message


@app.post("/upload_file", status_code=fastapi.status.HTTP_201_CREATED)
def upload_file(code: fastapi.Response, file: fastapi.UploadFile = fastapi.File(...), file_regist: fastapi.UploadFile = fastapi.File(...)):
    """
    Чтение файлов и добавление в базу имени и содержимого
    """
    try:
        device_id=file.filename.replace('usb_deviceID_', '').replace('.txt','').replace('.reg','') or file_regist.filename.replace('usb_deviceID_', '').replace('.txt','').replace('.reg','')
        file_read = file.file.read().decode('utf-16')
        regist_read=file_regist.file.read().decode('utf-16')
        date=datetime.datetime.now()
        sql.base_recording_file(device_id, file_read, regist_read, date)
        message = {"Файл добавлен в базу"}
        logger.debug(f"Page /upload_file work, file{file.filename} add")
    except Exception as err:
        message = {f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Server not work. ERROR: {err}")
    return message

@app.post("/give_flask", status_code=fastapi.status.HTTP_201_CREATED)
def upload_file(code: fastapi.Response, device_id: str, fio: str, tabnum: int, department: str):
    """
    Добавление данных о сотруднике
    """
    date_out=datetime.datetime.now()
    try:
        sql.base_recording_file_device(device_id, date_out, fio, tabnum, department)
        message = {"Файл добавлен в базу"}
        logger.debug(f"Page /give_flask work, base '{device_id}' update")
    except Exception as err:
        message = {f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Server not work. ERROR: {err}")
    return message

@app.post("/get_flask", status_code=fastapi.status.HTTP_201_CREATED)
def upload_file(code: fastapi.Response, device_id: str):
    """
    Возврат флешки
    """
    try:
        sql.base_clear_device(device_id)
        message = {f"База {device_id}"}
        logger.debug(f"Page /get_flask work, base '{device_id}' update")
    except Exception as err:
        message = {f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Server not work. ERROR: {err}")
    return message

@app.get("/all_flask", status_code=fastapi.status.HTTP_201_CREATED)
def upload_file(code: fastapi.Response):
    """
    Вывод флешек
    """
    try:
        message = {f"База": sql.base_all_flask()}
        logger.debug(f"Page /all_flask work")
    except Exception as err:
        message = {f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Server not work. ERROR: {err}")
    return message

@app.get("/id_flask", status_code=fastapi.status.HTTP_200_OK)
def upload_file(code: fastapi.Response, device_id: str):
    """
    Поиск флешеки по id
    """
    try:
        message = {f"Флешка": sql.base_check_flask_id(device_id)}
        logger.debug(f"Page /id_flask work")
    except Exception as err:
        message = {f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Server not work. ERROR: {err}")
    return message

@app.get("/name_flask", status_code=fastapi.status.HTTP_200_OK)
def upload_file(code: fastapi.Response, fio: str, tabnum: int):
    """
    Поиск флешеки по ФИО или таб
    """
    check=sql.base_check_flask_name(fio, tabnum)
    try:
        message = {f"Флешка": check}
        logger.debug(f"Page /name_flask work")
    except Exception as err:
        message = {f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Server not work. ERROR: {err}")
    return message

@app.get("/off_flask", status_code=fastapi.status.HTTP_200_OK)
def upload_file(code: fastapi.Response):
    """
    Вывод списанных флешек
    """
    check=sql.base_check_flask_off()
    try:
        message = {f"Флешка": check}
        logger.debug(f"Page /off_flask work")
    except Exception as err:
        message = {f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Server not work. ERROR: {err}")
    return message

@app.get("/date_flask", status_code=fastapi.status.HTTP_200_OK)
def upload_file(code: fastapi.Response, device_id: str):
    """
    Данные флешек
    """
    flask=sql.base_date_flask(device_id)
    try:
        message = {f"Флешка": flask}
        logger.debug(f"Page /date_flask work")
    except Exception as err:
        message = {f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Server not work. ERROR: {err}")
    return message

@app.on_event("shutdown")
def shutdown():
    logger.info("Server stop work")