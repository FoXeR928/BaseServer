import mimesis
import sqlite3
import sys
import pytest

from fastapi.testclient import TestClient

sys.path.append("./")
import app
from config import base, tabl

test_client = TestClient(app.app)


@pytest.yield_fixture(autouse=True)
def base_create():
    connect_sql = sqlite3.connect(f"{base}.db", timeout=5)
    curs = connect_sql.cursor()
    curs.execute(f"DELETE FROM {tabl}")
    curs.execute(
        f"""INSERT INTO {tabl}(device_id, device_path, device_reg, date_in, date_out, fio, tabnum, department)
                    VALUES ('name_one','text_txt','text_reg', '2011-10-13 16:23:16.083572',NULL,NULL,NULL,NULL),
                    ('name2','text_txt','text_reg','2011-10-13 16:23:16.083572','2019-03-07 23:17:50.848051','Кетрин Чимоканова',359254064417561,'Режиссер'),
                    ('name3','text_txt','text_reg','2011-10-13 16:23:16.083572','2019-03-07 23:17:50.848051',NULL,NULL,NULL),
                    ('name4','text_txt','text_reg','2011-10-13 16:23:16.083572','2019-03-07 23:17:50.848051','Велигор Миссюров',353166055808564,'Травматолог'),
                    ('name5','text_txt','text_reg','2011-10-13 16:23:16.083572','2019-03-07 23:17:50.848051','Хосе Подюков',329304008876062,'Психиатр'),
                    ('name6','text_txt','text_reg','2011-10-13 16:23:16.083572','2019-03-07 23:17:50.848051','Ынтымак Горляков',358240054017520,'Кассир');"""
    )
    connect_sql.commit()
    yield


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
    assert responses.json() == ["Добавлено в базу, если не было"]


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
    assert responses.json() == ["Добавлено в базу, если не было"]


def test_false_upload_file():
    files = [
        ("file_txt", (open("tests/test_file/usb_deviceID_name_one.txt", "rb"))),
        ("file_reg", (open("tests/test_file/usb_deviceID_name_one.reg", "rb"))),
    ]
    responses = test_client.post("/upload_file", files=files)
    assert responses.status_code == 201
    assert responses.json() == ["Добавлено в базу, если не было"]


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
    assert responses.json() == {"Флешка": [["text_txt", "text_reg"]]}


def test_give_file():
    device_id = "7"
    fio = ru.full_name()
    tabnum = gen.code.imei()
    department = ru.occupation()
    responses = test_client.post(
        f"/give_flask?device_id={device_id}&fio={fio}&tabnum={tabnum}&department={department}"
    )
    assert responses.status_code == 201
    assert responses.json() == [f"Флешка {device_id} выдана {fio}"]


def test_true_give_file():
    responses = test_client.post(
        "/give_flask?device_id=name_one&fio=1&tabnum=1&department=1"
    )
    assert responses.status_code == 201
    assert responses.json() == ["Флешка name_one выдана 1"]


def test_device_id_get():
    responses = test_client.post("/get_flask?device_id=1")
    assert responses.status_code == 201
    assert responses.json() == ["База флешки 1 очищена"]


def test_true_device_id_get():
    responses = test_client.post("/get_flask?device_id=name_one")
    assert responses.status_code == 201
    assert responses.json() == ["База флешки name_one очищена"]


def test_code_flask_off():
    responses = test_client.get("/off_flask")
    assert responses.status_code == 200
    assert responses.json() == {
        "Флешка": [
            [
                "name3",
                "text_txt",
                "text_reg",
                "2011-10-13 16:23:16.083572",
                "2019-03-07 23:17:50.848051",
                None,
                None,
                None,
            ]
        ]
    }


def test_code_flask_all():
    responses = test_client.get("/all_flask")
    assert responses.status_code == 200
    assert responses.json() == {
        "База": [
            [
                "name_one",
                "text_txt",
                "text_reg",
                "2011-10-13 16:23:16.083572",
                None,
                None,
                None,
                None,
            ],
            [
                "name2",
                "text_txt",
                "text_reg",
                "2011-10-13 16:23:16.083572",
                "2019-03-07 23:17:50.848051",
                "Кетрин Чимоканова",
                359254064417561,
                "Режиссер",
            ],
            [
                "name3",
                "text_txt",
                "text_reg",
                "2011-10-13 16:23:16.083572",
                "2019-03-07 23:17:50.848051",
                None,
                None,
                None,
            ],
            [
                "name4",
                "text_txt",
                "text_reg",
                "2011-10-13 16:23:16.083572",
                "2019-03-07 23:17:50.848051",
                "Велигор Миссюров",
                353166055808564,
                "Травматолог",
            ],
            [
                "name5",
                "text_txt",
                "text_reg",
                "2011-10-13 16:23:16.083572",
                "2019-03-07 23:17:50.848051",
                "Хосе Подюков",
                329304008876062,
                "Психиатр",
            ],
            [
                "name6",
                "text_txt",
                "text_reg",
                "2011-10-13 16:23:16.083572",
                "2019-03-07 23:17:50.848051",
                "Ынтымак Горляков",
                358240054017520,
                "Кассир",
            ],
        ]
    }


def test_false_name_flask():
    responses = test_client.get("/name_flask?fiotab=n")
    assert responses.status_code == 404
    assert responses.json() == ["Нету такой флешки"]


def test_true_name_flask():
    responses = test_client.get("/name_flask?fiotab=Велигор Миссюров")
    assert responses.status_code == 200
    assert responses.json() == {
        "Флешка": [
            [
                "name4",
                "text_txt",
                "text_reg",
                "2011-10-13 16:23:16.083572",
                "2019-03-07 23:17:50.848051",
                "Велигор Миссюров",
                353166055808564,
                "Травматолог",
            ]
        ]
    }


def test_true_tabnum_flask():
    responses = test_client.get("/name_flask?fiotab=358240054017520")
    assert responses.status_code == 200
    assert responses.json() == {
        "Флешка": [
            [
                "name6",
                "text_txt",
                "text_reg",
                "2011-10-13 16:23:16.083572",
                "2019-03-07 23:17:50.848051",
                "Ынтымак Горляков",
                358240054017520,
                "Кассир",
            ]
        ]
    }


def test_name_flask_only_one_letter():
    responses = test_client.get("/name_flask?fiotab=В")
    assert responses.status_code == 200
    assert responses.json() == {
        "Флешка": [
            [
                "name4",
                "text_txt",
                "text_reg",
                "2011-10-13 16:23:16.083572",
                "2019-03-07 23:17:50.848051",
                "Велигор Миссюров",
                353166055808564,
                "Травматолог",
            ]
        ]
    }


def test_tabnum_flask_only_one_number():
    responses = test_client.get("/name_flask?fiotab=3")
    assert responses.status_code == 200
    assert responses.json() == {
        "Флешка": [
            [
                "name2",
                "text_txt",
                "text_reg",
                "2011-10-13 16:23:16.083572",
                "2019-03-07 23:17:50.848051",
                "Кетрин Чимоканова",
                359254064417561,
                "Режиссер",
            ],
            [
                "name4",
                "text_txt",
                "text_reg",
                "2011-10-13 16:23:16.083572",
                "2019-03-07 23:17:50.848051",
                "Велигор Миссюров",
                353166055808564,
                "Травматолог",
            ],
            [
                "name5",
                "text_txt",
                "text_reg",
                "2011-10-13 16:23:16.083572",
                "2019-03-07 23:17:50.848051",
                "Хосе Подюков",
                329304008876062,
                "Психиатр",
            ],
            [
                "name6",
                "text_txt",
                "text_reg",
                "2011-10-13 16:23:16.083572",
                "2019-03-07 23:17:50.848051",
                "Ынтымак Горляков",
                358240054017520,
                "Кассир",
            ],
        ]
    }
