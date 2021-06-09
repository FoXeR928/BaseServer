import fastapi
from loguru import logger
import sql
import datetime
from config import tabl


app = fastapi.FastAPI()


@app.on_event("startup")
def start():
    logger.info("Server work")


def check_result(code, check):
    if check["err"] == 1:
        message = {"Нету такой флешки"}
        code.status_code = fastapi.status.HTTP_404_NOT_FOUND
    elif check["err"] == 0:
        message = {"Флешка": check["result"]}
        code.status_code = fastapi.status.HTTP_200_OK
    return {"code": code, "message": message}


@app.post("/upload_file", status_code=fastapi.status.HTTP_201_CREATED)
def upload_file(
    code: fastapi.Response,
    file_txt: fastapi.UploadFile = fastapi.File(...),
    file_reg: fastapi.UploadFile = fastapi.File(...),
):
    """
    Чтение содержимого файлов и добавление в базу id и содержимого
    """
    device_id1 = (
        file_txt.filename.replace("usb_deviceID_", "")
        .replace(".txt", "")
        .replace(".reg", "")
    )
    device_id2 = (
        file_reg.filename.replace("usb_deviceID_", "")
        .replace(".txt", "")
        .replace(".reg", "")
    )
    if (
        "usb_deviceID_" in (file_txt.filename and file_reg.filename)
        and device_id1 == device_id2
    ):
        read_reg = file_reg
        read_txt = file_txt
        if ".reg" in file_txt.filename and ".txt" in file_reg.filename:
            read_reg = file_txt
            read_txt = file_reg

        date = datetime.datetime.now()
        if (".reg" in file_txt.filename and ".reg" in file_reg.filename) or (
            ".txt" in file_txt.filename and ".txt" in file_reg.filename
        ):
            code.status_code = fastapi.status.HTTP_206_PARTIAL_CONTENT
            message = {"Вы добавили 2 файла с одинаковыми расширениями"}
        elif ".txt" in read_txt.filename and ".reg" in read_reg.filename:
            file_read = read_txt.file.read().decode("utf-16")
            regist_read = read_reg.file.read().decode("utf-16")
            result = sql.write_to_database_flash_drive(
                tabl, device_id1, file_read, regist_read, date
            )
            if result["err"] == 1:
                message = {f"Ошибка: {result['result']}"}
                code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
            elif result["err"] == 0:
                message = {"Добавлено в базу"}
        else:
            message = {"Не поддерживаемый формат файла"}
            code.status_code = fastapi.status.HTTP_400_BAD_REQUEST

    else:
        code.status_code = fastapi.status.HTTP_400_BAD_REQUEST
        message = {"Не верное название файла"}
    return message


@app.post("/give_flask", status_code=fastapi.status.HTTP_201_CREATED)
def give_file(
    code: fastapi.Response, device_id: str, fio: str, tabnum: int, department: str
):
    """
    Добавление данных о сотруднике к флешке
    """
    date_out = datetime.datetime.now()
    try:
        result = sql.write_to_database_issuing_flash_drive(
            tabl, device_id, date_out, fio, tabnum, department
        )
        if result["err"] == 1:
            message = {f"Ошибка: {result['result']}"}
            code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        elif result["err"] == 0:
            message = {f"Флешка {device_id} выдана {fio}"}
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
        result = sql.cleaning_resulting_flash_drive(tabl, device_id)
        if result["err"] == 1:
            message = {f"Ошибка: {result['result']}"}
            code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        elif result["err"] == 0:
            message = {f"База флешки {device_id} очищена"}
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
        check = sql.all_flash_drives_of_base(tabl)
        if check["err"] == 0:
            message = {"База": check["result"]}
        logger.debug("Page /all_flask work")
    except Exception as err:
        message = {f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Server not work. ERROR: {err}")
    return message


@app.get("/id_flask", status_code=fastapi.status.HTTP_200_OK)
def id_flask(code: fastapi.Response, device_id: str):
    """
    Поиск флешки по id
    """
    try:
        check = sql.search_flash_drive_based_on_id(tabl, device_id)
        result = check_result(code, check)
        message = result["message"]
        logger.debug("Page /id_flask work")
    except Exception as err:
        message = {f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Server not work. ERROR: {err}")
    return message


@app.get("/name_flask", status_code=fastapi.status.HTTP_200_OK)
def name_flask(code: fastapi.Response, fio: str):
    """
    Поиск флешки по ФИО
    """
    try:
        check = sql.search_flash_drive_based_on_fio(tabl, fio)
        result = check_result(code, check)
        message = result["message"]
        logger.debug("Page /name_flask work")
    except Exception as err:
        message = {f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Server not work. ERROR: {err}")
    return message


@app.get("/tabnum_flask", status_code=fastapi.status.HTTP_200_OK)
def tabnum_flask(code: fastapi.Response, tabnum: int):
    """
    Поиск флешки по табельному номеру
    """
    try:
        check = sql.search_flash_drive_based_on_tadnum(tabl, tabnum)
        result = check_result(code, check)
        message = result["message"]
        logger.debug("Page /name_flask work")
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
    try:
        check = sql.search_decommissioned_flash_drives(tabl)
        result = check_result(code, check)
        message = result["message"]
        logger.debug("Page /off_flask work")
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
    flask = sql.file_search_based_on_id(tabl, device_id)
    try:
        result = check_result(code, flask)
        message = result["message"]
        logger.debug(f"Page /date_flask work")
    except Exception as err:
        message = {f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Server not work. ERROR: {err}")
    return message


@app.on_event("shutdown")
def shutdown():
    logger.info("Server stop work")
