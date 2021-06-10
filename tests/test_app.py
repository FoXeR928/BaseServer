from datetime import datetime
import mimesis
import sqlite3
import sys
import pytest

from fastapi.testclient import TestClient

sys.path.append("./")
import app
from config import base, tabl
from sql import open_base

test_client = TestClient(app.app)


code_200 = 200
code_201 = 201
code_206 = 206
code_400 = 400
code_404 = 404
code_422 = 422


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
    assert responses.status_code == code_201
    assert responses.json() == ["Added to base"]
    curs = open_base(base)
    curs.execute(
        f"SELECT device_id, device_path, device_reg FROM {tabl} WHERE device_id='P1601450070867E90D1B6300'"
    )
    result = curs.fetchall()
    assert result == [
        (
            "P1601450070867E90D1B6300",
            "Здесь сообщение, которое проверяет правильность записи в базу, но сообщение я не придумал поэтому psoskgepgodfle[porypoyietor[glhkrpoyitrpyglkfg;hnmf]]",
            "А тут написан другой текст для проверки работоспособности записи в базу и текст этот из себя представляет p[rtier0934-0534lkjfldfgt3048po;egkdhdlgypeortyiglmmdbr454k]",
        )
    ]


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
    assert responses.status_code == code_201
    assert responses.json() == ["Added to base"]


def test_false_upload_file():
    files = [
        ("file_txt", (open("tests/test_file/usb_deviceID_name_one.txt", "rb"))),
        ("file_reg", (open("tests/test_file/usb_deviceID_name_one.reg", "rb"))),
    ]
    responses = test_client.post("/upload_file", files=files)
    assert responses.status_code == code_422
    assert responses.json() == ['ERROR: UNIQUE constraint failed: tabl.device_id']


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
    assert responses.status_code == code_206
    assert responses.json() == ["You have added 2 files with the same extensions"]


def test_false3_upload_file():
    responses = test_client.post(
        "/upload_file",
        files={
            "file_txt": "usb_deviceID_name_one.txt",
            "file_reg": "usb_deviceID_P1601450070867E90D1B6301.reg",
        },
    )
    assert responses.status_code == code_400
    assert responses.json() == ["Incorrect file name"]


def test_upload_file():
    responses = test_client.post(
        "/upload_file", files={"file_txt": "1", "file_reg": "1"}
    )
    assert responses.status_code == code_400
    assert responses.json() == ["Incorrect file name"]


def test_device_id_date():
    responses = test_client.get("/date_flask/?device_id=1")
    assert responses.status_code == code_404
    assert responses.json() == ["Not result"]


def test_true_device_id_date():
    responses = test_client.get("/date_flask/?device_id=name_one")
    assert responses.status_code == code_200
    assert responses.json() == {"Flask": [["text_txt", "text_reg"]]}


def test_give_file():
    device_id = "7"
    fio = ru.full_name()
    tabnum = gen.code.imei()
    department = ru.occupation()
    responses = test_client.put(
        f"/give_flask?device_id={device_id}&fio={fio}&tabnum={tabnum}&department={department}"
    )
    assert responses.status_code == code_422
    assert responses.json() == [f"Flask {device_id} give to {fio}"]


def test_true_give_file():
    responses = test_client.put(
        "/give_flask?device_id=name_one&fio=1&tabnum=1&department=1"
    )
    assert responses.status_code == code_201
    assert responses.json() == ["Flask name_one give to 1"]


def test_device_id_get():
    responses = test_client.put("/get_flask?device_id=1")
    assert responses.status_code == code_422
    assert responses.json() == ["Flash drive base 1 cleared"]


def test_true_device_id_get():
    responses = test_client.put("/get_flask?device_id=name_one")
    assert responses.status_code == code_201
    assert responses.json() == ["Flash drive base name_one cleared"]


def test_code_flask_off():
    responses = test_client.get("/off_flask")
    assert responses.status_code == code_200
    assert responses.json() == {
        "Flask": [
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
    assert responses.status_code == code_200
    assert responses.json() == {
        "Base": [
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
    responses = test_client.get("/name_flask?fio=n")
    assert responses.status_code == code_404
    assert responses.json() == ["Not result"]


def test_true_name_flask():
    responses = test_client.get("/name_flask?fio=Велигор Миссюров")
    assert responses.status_code == code_200
    assert responses.json() == {
        "Flask": [
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
    responses = test_client.get("/tabnum_flask?tabnum=358240054017520")
    assert responses.status_code == code_200
    assert responses.json() == {
        "Flask": [
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
    responses = test_client.get("/name_flask?fio=В")
    assert responses.status_code == code_200
    assert responses.json() == {
        "Flask": [
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
    responses = test_client.get("/tabnum_flask?tabnum=3")
    assert responses.status_code == code_200
    assert responses.json() == {
        "Flask": [
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
