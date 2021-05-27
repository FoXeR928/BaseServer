import fastapi
import logs
from loguru import logger
from config import load_config
import sql

# Добавлени параметров логов
logs.init_log()
# Инициализация fastapi
app = fastapi.FastAPI()
user = load_config()


@app.on_event("startup")
def start():
    logger.info("Server work")


# Запуск страницы info
@app.get("/info")
def root():
    # Сообщение о работе страницы
    logger.info("Page info work")
    message = {"message": "Привет"}
    return message


@app.post("/user_post/", status_code=fastapi.status.HTTP_201_CREATED)
def post_user(name: str, surename: str, patronymic: str, code: fastapi.Response):
    try:
        message = sql.base_recording(name, surename, patronymic)
    except Exception as err:
        message = str(err)
        logger.error(f"Server not work. ERROR: {err}")
        code.status_code = fastapi.status.HTTP_501_NOT_IMPLEMENTED
    return message


@app.get("/user/{surename}", status_code=fastapi.status.HTTP_200_OK)
def name(surename: str, code: fastapi.Response):
    try:
        name = sql.base_check(surename)
        for name in name:
            message = {"message": f"Привет {name[0]} {name[1]} {name[2]}"}
        logger.info(f"Page user/{surename} work")
    except Exception as err:
        message = str(err)
        logger.error(f"Server not work. ERROR: {err}")
        code.status_code = fastapi.status.HTTP_404_NOT_FOUND
    return message

@app.post("/upload_file", status_code=fastapi.status.HTTP_201_CREATED)
def upload_file(code: fastapi.Response, file: fastapi.UploadFile=fastapi.File(...)):
    try:
        sql.base_recording_file(file.filename, file.content_type)
        message={"Файл добавлен в базу"}
    except Exception as err:
        message={f"Ошибка: {err}"}
        code.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    return message

        

@app.on_event("shutdown")
def shutdown():
    logger.info("Server stop work")
