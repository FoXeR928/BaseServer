import mimesis
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append("./")
import app
from db_set import tabl, base
import sql

test_client = TestClient(app.app)


def open_base():
    engine = create_engine("sqlite:///flask-date.db")
    base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


@pytest.yield_fixture(autouse=True)
def base_create():
    session = open_base()
    session.query(tabl).delete()
    record = (tabl(device_id="name_one", device_path="1", device_reg="1", date_in="1"),)
    record2 = (
        tabl(
            device_id="name2",
            device_path="2",
            device_reg="2",
            date_in="2",
            date_out="2",
            fio="2",
            tabnum="2",
            department="2",
        ),
    )
    record3 = (
        tabl(
            device_id="3",
            device_path="3",
            device_reg="3",
            date_in="3",
            date_out="3",
            fio="3",
        ),
    )
    record4 = (
        tabl(
            device_id="4",
            device_path="4",
            device_reg="4",
            date_in="4",
            date_out="four",
            fio="four",
            tabnum="4",
            department="four",
        ),
    )
    record5 = (
        tabl(
            device_id="5",
            device_path="5",
            device_reg="5",
            date_in="5",
            date_out="five",
            fio="5",
            tabnum="five",
            department="five",
        ),
    )
    record6 = tabl(
        device_id="six",
        device_path="6",
        device_reg="6",
        date_in="6",
        date_out="6",
        fio="6",
        tabnum="6",
        department="6",
    )
    session.add([record, record2, record3, record4, record5, record6])
    session.commit()


en = mimesis.Person("en")
ru = mimesis.Person("ru")
cod_status = mimesis.Internet("en")
gen = mimesis.Generic("en")


def test_true_upload_file():
    files = [
        (
            "file_txt",
            (open("tests/test_file/usb_deviceID_P1601450070867E90D1B6300.txt", "rb")),
        ),
        (
            "file_reg",
            (open("tests/test_file/usb_deviceID_P1601450070867E90D1B6300.reg", "rb")),
        ),
    ]
    responses = test_client.post("/upload_file", files=files)
    assert responses.status_code == 201
    assert responses.json() == ["Добавлено в базу"]


def test_true_2_upload_file():
    files = [
        (
            "file_txt",
            (open("tests/test_file/usb_deviceID_P1601450070867E90D1B6309.reg", "rb")),
        ),
        (
            "file_reg",
            (open("tests/test_file/usb_deviceID_P1601450070867E90D1B6309.txt", "rb")),
        ),
    ]
    responses = test_client.post("/upload_file", files=files)
    assert responses.status_code == 201
    assert responses.json() == ["Добавлено в базу"]


def test_false_upload_file():
    files = [
        ("file_txt", (open("tests/test_file/usb_deviceID_name_one.txt", "rb"))),
        ("file_reg", (open("tests/test_file/usb_deviceID_name_one.reg", "rb"))),
    ]
    responses = test_client.post("/upload_file", files=files)
    assert responses.status_code == 208
    assert responses.json() == ["Уже есть в базе name_one"]


def test_false_2_upload_file():
    files = [
        (
            "file_txt",
            (open("tests/test_file/usb_deviceID_P1601450070867E90D1B6300.reg", "rb")),
        ),
        (
            "file_reg",
            (open("tests/test_file/usb_deviceID_P1601450070867E90D1B6300.reg", "rb")),
        ),
    ]
    responses = test_client.post("/upload_file", files=files)
    assert responses.status_code == 206
    assert responses.json() == ["Вы добавили 2 файла с одинаковыми расширениями"]


def test_false3_upload_file():
    responses = test_client.post(
        "/upload_file",
        files={
            "file_txt": "usb_deviceID_name_one.txt",
            "file_reg": "usb_deviceID_P1601450070867E90D1B6301.reg",
        },
    )
    assert responses.status_code == 400
    assert responses.json() == ["Не верное название файла"]


def test_upload_file():
    responses = test_client.post(
        "/upload_file", files={"file_txt": "1", "file_reg": "1"}
    )
    assert responses.status_code == 400
    assert responses.json() == ["Не верное название файла"]


# def test_upload_file():
#     responses = test_client.post("/upload_file", files={"files": "1", "files": "1"})
#     assert responses.status_code == 201
#     assert responses.json() == ["Не верное название файла"]


# def test_reg_upload_file():
#     responses = test_client.post(
#         "/upload_file",
#         files={
#             "files": open(
#                 "tests/test_file/usb_deviceID_P1601450070867E90D1B6300.reg", "rb"
#             )
#         },
#     )
#     assert responses.status_code == 201
#     assert responses.json() == [
#         "Файла .reg [] и .txt ['usb_deviceID_P1601450070867E90D1B6300'] не хватает"
#     ]


# def test_txt_upload_file():
#     responses = test_client.post(
#         "/upload_file",
#         files={
#             "files": open(
#                 "tests/test_file/usb_deviceID_P1601450070867E90D1B6300.txt", "rb"
#             )
#         },
#     )
#     assert responses.status_code == 201
#     assert responses.json() == [
#         "Файла .reg ['usb_deviceID_P1601450070867E90D1B6300'] и .txt [] не хватает"w
#     ]


# def test_all_upload_file():
#     files = [
#         "files",
#         open("tests/test_file/usb_deviceID_P1601450070867E90D1B6300.reg", "rb"),
#         "files",
#         open("tests/test_file/usb_deviceID_P1601450070867E90D1B6300.txt", "rb"),
#     ]
#     responses = test_client.post("/upload_file", files=files)
#     assert responses.status_code == 201
#     assert responses.json() == ["Файл добавлен в базу"]


def test_device_id_date():
    responses = test_client.get("/date_flask/?device_id=1")
    assert responses.status_code == 404
    assert responses.json() == ["Нету такой флешки"]


def test_true_device_id_date():
    responses = test_client.get("/date_flask/?device_id=name_one")
    assert responses.status_code == 200
    assert responses.json() == {"Флешка": [["1", "1"]]}


def test_give_file():
    device_id = en.password()
    fio = ru.full_name()
    tabnum = gen.code.imei()
    department = ru.occupation()
    responses = test_client.post(
        f"/give_flask?device_id={device_id}&fio={fio}&tabnum={tabnum}&department={department}"
    )
    assert responses.status_code == 404
    assert responses.json() == ["Не найдено id"]


def test_true_give_file():
    responses = test_client.post(
        "/give_flask?device_id=name_one&fio=1&tabnum=1&department=1"
    )
    assert responses.status_code == 201
    assert responses.json() == ["Флешка name_one выдана 1"]


def test_device_id_get():
    responses = test_client.post("/get_flask?device_id=1")
    assert responses.status_code == 404
    assert responses.json() == ["Данных и так нет"]


def test_device_id_get():
    responses = test_client.post("/get_flask?device_id=name_one")
    assert responses.status_code == 201
    assert responses.json() == ["База флешки name_one очищена"]


def test_device_id():
    responses = test_client.get("/id_flask/?device_id=1")
    assert responses.status_code == 404
    assert responses.json() == ["Нету такой флешки"]


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
    assert responses.status_code == 404
    assert responses.json() == ["Нету такой флешки"]


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
