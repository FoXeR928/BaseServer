import mimesis
import sqlite3
import sys

sys.path.append("./")
import app
from fastapi.testclient import TestClient
from config import load_config

cfg = load_config()

test_client = TestClient(app.app)


def base_create():
    connect_sql = sqlite3.connect(f"{cfg.base}.db", timeout=5)
    curs = connect_sql.cursor()
    curs.execute(f"DELETE FROM {cfg.tabl_file}")
    curs.execute(
        f"""INSERT INTO {cfg.tabl_file}(device_id, device_path, device_reg, date_in, date_out, fio, tabnum, department)
                    VALUES ('name_one','1','1','1',NULL,NULL,NULL,NULL),
                    ('name2','2','2','2','2','2','2','2'),
                    ('3','3','3','3','3',NULL,NULL,NULL),
                    ('4',4,4,4,'four','four',4,'four'),
                    ('5',5,5,5,'five',5,'five','five'),
                    ('six',6,6,6,6,6,6,6);"""
    )
    connect_sql.commit()


base_create()

en = mimesis.Person("en")
ru = mimesis.Person("ru")
cod_status = mimesis.Internet("en")
gen = mimesis.Generic("en")

def test_upload_file():
    responses = test_client.post("/upload_file",files={"files":'1',"files": '1'})
    assert responses.status_code == 201
    assert responses.json() == ['Не верное название файла']

def test_reg_upload_file():
    responses = test_client.post("/upload_file",files={'files': open('tests/test_file/usb_deviceID_P1601450070867E90D1B6300.reg', 'rb')})
    assert responses.status_code == 201
    assert responses.json() == ["Файла .reg [] и .txt ['usb_deviceID_P1601450070867E90D1B6300'] не хватает"]

def test_txt_upload_file():
    responses = test_client.post("/upload_file",files={'files': open('tests/test_file/usb_deviceID_P1601450070867E90D1B6300.txt', 'rb')})
    assert responses.status_code == 201
    assert responses.json() == ["Файла .reg ['usb_deviceID_P1601450070867E90D1B6300'] и .txt [] не хватает"]

def test_all_upload_file():
    responses = test_client.post("/upload_file",files={'files': (open('tests/test_file/usb_deviceID_P1601450070867E90D1B6300.reg', 'rb') and open('tests/test_file/usb_deviceID_P1601450070867E90D1B6300.txt', 'rb'))})
    assert responses.status_code == 201
    assert responses.json() == ["Файл добавлен в базу"]


def test_device_id_date():
    responses = test_client.get("/date_flask/?device_id=1")
    assert responses.status_code == 200
    assert responses.json() == {"Флешка": "Такого в базе нету"}


def test_true_device_id_date():
    responses = test_client.get("/date_flask/?device_id=name_one")
    assert responses.status_code == 200
    assert responses.json() == {"Флешка": [["1", "1"]]}


def test_give_file():
    cod = cod_status.http_status_code()
    device_id = en.password()
    fio = ru.full_name()
    tabnum = gen.code.imei()
    department = ru.occupation()
    assert app.give_file(cod, device_id, fio, tabnum, department) == {
        "Такого нет в базе"
    }


def test_true_give_file():
    responses = test_client.post(
        "/give_flask?device_id=name_one&fio=1&tabnum=1&department=1"
    )
    assert responses.status_code == 201
    assert responses.json() == ["Флешка выдана"]


def test_device_id_get():
    responses = test_client.post("/get_flask?device_id=1")
    assert responses.status_code == 201
    assert responses.json() == ["Данных и так нет"]


def test_device_id_get():
    responses = test_client.post("/get_flask?device_id=name_one")
    assert responses.status_code == 201
    assert responses.json() == ["Флешка очищена"]


def test_device_id():
    responses = test_client.get("/id_flask/?device_id=1")
    assert responses.status_code == 200
    assert responses.json() == {"Флешка": "Такой в базе нету"}


def test_code_flask_off():
    responses = test_client.get("/off_flask")
    assert responses.status_code == 200
    assert responses.json() == {"Флешка": [["3", "3", "3", 3, 3, None, None, None]]}


def test_code_flask_all():
    responses = test_client.get("/all_flask")
    assert responses.status_code == 200
    assert responses.json() == {
        "База": [
            ["name_one", "1", "1", 1, None, None, None, None],
            ["name2", "2", "2", 2, 2, "2", 2, "2"],
            ["3", "3", "3", 3, 3, None, None, None],
            ["4", "4", "4", 4, "four", "four", 4, "four"],
            ["5", "5", "5", 5, "five", "5", "five", "five"],
            ["six", "6", "6", 6, 6, "6", 6, "6"],
        ]
    }


def test_name_flask():
    responses = test_client.get("/name_flask?fiotab=1")
    assert responses.status_code == 200
    assert responses.json() == {"Флешка": "Такого в базе нету"}


def test_true_name_flask():
    responses = test_client.get("/name_flask?fiotab=four")
    assert responses.status_code == 200
    assert responses.json() == {
        "Флешка": [["4", "4", "4", 4, "four", "four", 4, "four"]]
    }


def test_true_tabnum_flask():
    responses = test_client.get("/name_flask?fiotab=five")
    assert responses.status_code == 200
    assert responses.json() == {
        "Флешка": [["5", "5", "5", 5, "five", "5", "five", "five"]]
    }
