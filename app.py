import fastapi
from loguru import logger
import sql
import datetime
from config import tabl
# import typing

app = fastapi.FastAPI()


@app.on_event("startup")
def start():
    logger.info("Server work")


@app.post("/upload_file", status_code=fastapi.status.HTTP_201_CREATED)
def upload_file(
    code: fastapi.Response,
    file_txt: fastapi.UploadFile = fastapi.File(...),
    file_reg: fastapi.UploadFile = fastapi.File(...),
):
    """
    Чтение содержимого файлов и добавление в базу имени и содержимого
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
                device_id1, file_read, regist_read, date
            )
            if result[0] == 208:
                message = {f"Уже есть в базе {device_id1}"}
                code.status_code = fastapi.status.HTTP_208_ALREADY_REPORTED
            elif result[0] == 201:
                message = {"Добавлено в базу"}
        else:
            message = {"Не поддерживаемый формат файла"}
            code.status_code = fastapi.status.HTTP_400_BAD_REQUEST

    else:
        code.status_code = fastapi.status.HTTP_400_BAD_REQUEST
        message = {"Не верное название файла"}
    return message


# @app.post("/upload_file", status_code=fastapi.status.HTTP_201_CREATED)
# def upload_file(
#     code: fastapi.Response,
#     files: typing.List[fastapi.UploadFile] = fastapi.File(...),
# ):
#     """
#     Чтение содержимого файлов и добавление в базу имени и содержимого
#     """
#     txt = []
#     reg = []
#     for file in files:
#         if "usb_deviceID_" in file.filename:
#             device_id = file.filename.replace("usb_deviceID_", "")
#             if ".txt" in file.filename:
#                 file_read = file.file.read().decode("utf-16")
#                 file = file.filename.replace(".txt", "")
#                 txt.append(file)
#             elif ".reg" in file.filename:
#                 regist_read = file.file.read().decode("utf-16")
#                 file = file.filename.replace(".reg", "")
#                 reg.append(file)
#             else:
#                 message = {"Не поддерживаемый формат файла"}
#             device_id = device_id.replace(".txt", "").replace(".reg", "")
#             if len(txt) > 0 and len(reg) > 0:
#                 for i in txt:
#                     i = i
#                 for x in reg:
#                     x = x
#                 if i == x:
#                     try:
#                         date = datetime.datetime.now()
#                         message = {
#                             sql.write_to_database_flash_drive(
#                                 device_id, file_read, regist_read, date
#                             )
#                         }
#                         logger.debug(f"Page /upload_file work, file {file} add")
#                     except Exception as err:
#                         message = {f"Ошибка: {err}"}
#                         code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
#                         logger.error(f"Server not work. ERROR: {err}")
#             else:
#                 message = {f"Файла .reg {txt} и .txt {reg} не хватает"}
#         else:
#             message = {"Не верное название файла"}
#     return message


@app.post("/give_flask", status_code=fastapi.status.HTTP_201_CREATED)
def give_file(
    code: fastapi.Response, device_id: str, fio: str, tabnum: int, department: str
):
    """
    Добавление данных о сотруднике
    """
    date_out = datetime.datetime.now()
    try:
        result = sql.write_to_database_issuing_flash_drive(
            device_id, date_out, fio, tabnum, department
        )
        if result[0] == 404:
            message = {"Не найдено id"}
            code.status_code = fastapi.status.HTTP_404_NOT_FOUND
        elif result[0] == 201:
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
        result = sql.cleaning_resulting_flash_drive(device_id)
        if result[0] == 404:
            message = {"Нету такой флешки"}
            code.status_code = fastapi.status.HTTP_404_NOT_FOUND
        elif result[0] == 201:
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
        check = sql.all_flash_drives_of_base()
        result = check[0]
        if result[0] == 200:
            message = {"База": check[1]}
        logger.debug("Page /all_flask work")
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
        check = sql.search_flash_drive_based_on_id(device_id)
        result = check[0]
        if check[0] == 404:
            message = {"Нету такой флешки"}
            code.status_code = fastapi.status.HTTP_404_NOT_FOUND
        elif result[0] == 200:
            message = {"Флешка": check[1]}
        logger.debug("Page /id_flask work")
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
    check = sql.search_flash_drive_based_on_fio_or_tadnumder(fiotab)
    result = check[0]
    try:
        if check[0] == 404:
            message = {"Нету такой флешки"}
            code.status_code = fastapi.status.HTTP_404_NOT_FOUND
        elif result[0] == 200:
            message = {"Флешка": check[1]}
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
    check = sql.search_decommissioned_flash_drives()
    result = check[0]
    try:
        if check[0] == 404:
            message = {"Нету такой флешки"}
            code.status_code = fastapi.status.HTTP_404_NOT_FOUND
        elif result[0] == 200:
            message = {"Флешка": check[1]}
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
    flask = sql.file_search_based_on_id(device_id)
    print(flask)
    result = flask[0]
    try:
        if flask[0] == 404:
            message = {"Нету такой флешки"}
            code.status_code = fastapi.status.HTTP_404_NOT_FOUND
        elif result[0] == 200:
            message = {"Флешка": flask[1]}
        logger.debug(f"Page /date_flask work")
    except Exception as err:
        message = {f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Server not work. ERROR: {err}")
    return message


@app.on_event("shutdown")
def shutdown():
    logger.info("Server stop work")
