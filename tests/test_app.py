import mimesis
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append("./")
import app
from db_set import Base, Tabl
import config

test_client = TestClient(app.app)


code_200 = 200
code_201 = 201
code_206 = 206
code_400 = 400
code_404 = 404
code_422 = 422


def open_base(base):
    sys.path.append("../")
    engine = create_engine(f"sqlite:///{base}.db")
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    open_base.engine = engine
    return session


@pytest.yield_fixture(autouse=True)
def base_create():
    session = open_base(config.base)
    session.query(Tabl).delete()
    session.commit()
    record = Tabl(
        device_id="name_one",
        device_path="text_txt",
        device_reg="text_reg",
        date_in="2011-10-13 16:23:16.083572",
    )
    record2 = Tabl(
        device_id="name2",
        device_path="text_txt",
        device_reg="text_reg",
        date_in="2011-10-13 16:23:16.083572",
        date_out="2019-03-07 23:17:50.848051",
        fio="Кетрин Чимоканова",
        tabnum=359254064417561,
        department="Режиссер",
    )
    record3 = Tabl(
        device_id="name3",
        device_path="text_txt",
        device_reg="text_reg",
        date_in="2011-10-13 16:23:16.083572",
        date_out="2019-03-07 23:17:50.848051",
    )
    record4 = Tabl(
        device_id="name4",
        device_path="text_txt",
        device_reg="text_reg",
        date_in="2011-10-13 16:23:16.083572",
        date_out="2019-03-07 23:17:50.848051",
        fio="Велигор Миссюров",
        tabnum=353166055808564,
        department="Травматолог",
    )
    record5 = Tabl(
        device_id="name5",
        device_path="text_txt",
        device_reg="text_reg",
        date_in="2011-10-13 16:23:16.083572",
        date_out="2019-03-07 23:17:50.848051",
        fio="Хосе Подюков",
        tabnum=329304008876062,
        department="Психиатр",
    )
    record6 = Tabl(
        device_id="name6",
        device_path="text_txt",
        device_reg="text_reg",
        date_in="2011-10-13 16:23:16.083572",
        date_out="2019-03-07 23:17:50.848051",
        fio="Ынтымак Горляков",
        tabnum=358240054017520,
        department="Кассир",
    )
    session.add_all([record, record2, record3, record4, record5, record6])
    session.commit()
    session.close()

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
    responses = test_client.get("/date_flask/?device_id=P1601450070867E90D1B6300")
    assert responses.status_code == code_200
    assert responses.json() == {
        "Flask": [
            "Здесь сообщение, которое проверяет правильность "
            "записи в базу, но сообщение я не придумал поэтому "
            "psoskgepgodfle[porypoyietor[glhkrpoyitrpyglkfg;hnmf]]",
            "А тут написан другой текст для проверки "
            "работоспособности записи в базу и текст этот из "
            "себя представляет "
            "p[rtier0934-0534lkjfldfgt3048po;egkdhdlgypeortyiglmmdbr454k]",
        ],
    }


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
    assert responses.json() == [
        """ERROR: (sqlite3.IntegrityError) UNIQUE constraint failed: tabl2.device_id\n[SQL: INSERT INTO tabl2 (device_id, device_path, device_reg, date_in, date_out, fio, tabnum, department) VALUES (?, ?, ?, ?, 
?, ?, ?, ?)]\n[parameters: ('name_one', 'ответ', 'ответ', datetime.datetime(2021, 6, 10, 10, 0, 11, 541568), None, None, None, None)]\n(Background on this error at: http://sqlalche.me/e/14/gkpj)"""
    ]


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


def test_true_search_device_id():
    responses = test_client.get("/id_flask?device_id=name_one")
    assert responses.status_code == code_200
    assert responses.json() == {
        "Flask": [
            [
                "name_one",
                "text_txt",
                "text_reg",
                "2011-10-13 16:23:16.083572",
                None,
                None,
                None,
                None,
            ]
        ],
    }


def test_false_search_device_id():
    responses = test_client.get("/id_flask?device_id=1")
    assert responses.status_code == code_404
    assert responses.json() == ["Not result"]


def test_device_id_date():
    responses = test_client.get("/date_flask/?device_id=1")
    assert responses.status_code == code_404
    assert responses.json() == ["Not result"]


def test_true_device_id_date():
    responses = test_client.get("/date_flask/?device_id=name_one")
    assert responses.status_code == code_200
    assert responses.json() == {"Flask": ["text_txt", "text_reg"]}


def test_give_file():
    device_id = "7"
    fio = ru.full_name()
    tabnum = gen.code.imei()
    department = ru.occupation()
    responses = test_client.put(
        f"/give_flask?device_id={device_id}&fio={fio}&tabnum={tabnum}&department={department}"
    )
    assert responses.status_code == code_422
    assert responses.json() == ["ERROR: No row was found when one was required"]


def test_true_give_file():
    responses = test_client.put(
        "/give_flask?device_id=name_one&fio=1&tabnum=1&department=1"
    )
    assert responses.status_code == code_201
    assert responses.json() == ["Flask name_one give to 1"]


def test_device_id_get():
    responses = test_client.put("/get_flask?device_id=1")
    assert responses.status_code == code_422
    assert responses.json() == ["ERROR: No row was found when one was required"]


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


def test_false_tabnum_flask():
    responses = test_client.get(
        "/tabnum_flask?tabnum=3333333333333333333333333333333333"
    )
    assert responses.status_code == code_404
    assert responses.json() == ["Not result"]


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
