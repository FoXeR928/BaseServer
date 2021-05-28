import fastapi
import logs
from loguru import logger
from config import load_config
import sql

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
def upload_file(code: fastapi.Response, file: fastapi.UploadFile = fastapi.File(...)):
    """
    Чтение файлов и добавление в базу имени и содержимого
    """
    try:
        file_read = file.file.read().decode()
        sql.base_recording_file(file.filename, file_read)
        message = {"Файл добавлен в базу"}
        logger.debug(f"Page user/upload_file work, file{file.filename} add")
    except Exception as err:
        message = {f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Server not work. ERROR: {err}")
    return message


@app.on_event("shutdown")
def shutdown():
    logger.info("Server stop work")
