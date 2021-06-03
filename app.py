import fastapi
from fastapi.params import Header
from loguru import logger
from config import load_config
import sql
import datetime
import typing

app = fastapi.FastAPI()
user = load_config()


@app.on_event("startup")
def start():
    logger.info("Server work")


@app.post("/upload_file", status_code=fastapi.status.HTTP_201_CREATED)
def upload_file(
    code: fastapi.Response,
    files: typing.List[fastapi.UploadFile] = fastapi.File(...),
):
    """
    Чтение содержимого файлов и добавление в базу имени и содержимого
    """
    txt = []
    reg = []
    for file in files:
        if "usb_deviceID_" in file.filename:
            device_id = file.filename.replace("usb_deviceID_", "")
            if ".txt" in file.filename:
                file_read = file.file.read().decode("utf-16")
                file = file.filename.replace(".txt", "")
                txt.append(file)
            elif ".reg" in file.filename:
                regist_read = file.file.read().decode("utf-16")
                file = file.filename.replace(".reg", "")
                reg.append(file)
            else:
                message = {"Не поддерживаемый формат файла"}
            device_id = device_id.replace(".txt", "").replace(".reg", "")
            if len(txt) > 0 and len(reg) > 0:
                for i in txt:
                    i = i
                for x in reg:
                    x = x
                if i == x:
                    txt.remove(i)
                    reg.remove(x)
                    try:
                        date = datetime.datetime.now()
                        message = {
                            sql.base_recording_file(
                                device_id, file_read, regist_read, date
                            )
                        }
                        logger.debug(f"Page /upload_file work, file {file} add")
                    except Exception as err:
                        message = {f"Ошибка: {err}"}
                        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
                        logger.error(f"Server not work. ERROR: {err}")
            else:
                message = {f"Файла .reg {txt} и .txt {reg} не хватает"}
        else:
            message = {"Не верное название файла"}
    return message


@app.post("/give_flask", status_code=fastapi.status.HTTP_201_CREATED)
def give_file(
    code: fastapi.Response, device_id: str, fio: str, tabnum: int, department: str
):
    """
    Добавление данных о сотруднике
    """
    date_out = datetime.datetime.now()
    try:
        sql.base_recording_file_device(device_id, date_out, fio, tabnum, department)
        message = {
            sql.base_recording_file_device(device_id, date_out, fio, tabnum, department)
        }
        logger.debug(f"Page /give_flask work, base '{device_id}' update")
    except Exception as err:
        message = {f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Server not work. ERROR: {err}")
    return message


@app.post("/get_flask", status_code=fastapi.status.HTTP_201_CREATED)
def get_flask(code: fastapi.Response, device_id: str):
    """
    Возврат флешки
    """
    try:
        message = {sql.base_clear_device(device_id)}
        logger.debug(f"Page /get_flask work, base '{device_id}' update")
    except Exception as err:
        message = {f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Server not work. ERROR: {err}")
    return message


@app.get("/all_flask", status_code=fastapi.status.HTTP_200_OK)
def all_flask(code: fastapi.Response):
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
def id_flask(code: fastapi.Response, device_id: str):
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
def name_flask(code: fastapi.Response, fiotab: str):
    """
    Поиск флешеки по ФИО или таб
    """
    check = sql.base_check_flask_name(fiotab)
    try:
        message = {f"Флешка": check}
        logger.debug(f"Page /name_flask work")
    except Exception as err:
        message = {f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Server not work. ERROR: {err}")
    return message


@app.get("/off_flask", status_code=fastapi.status.HTTP_200_OK)
def off_flask(code: fastapi.Response):
    """
    Вывод списанных флешек
    """
    check = sql.base_check_flask_off()
    try:
        message = {f"Флешка": check}
        logger.debug(f"Page /off_flask work")
    except Exception as err:
        message = {f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Server not work. ERROR: {err}")
    return message


@app.get("/date_flask", status_code=fastapi.status.HTTP_200_OK)
def date_flask(code: fastapi.Response, device_id: str):
    """
    Данные флешек
    """
    flask = sql.base_date_flask(device_id)
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
