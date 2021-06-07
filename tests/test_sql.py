import mimesis
import sqlite3
import sys
import pytest

sys.path.append("./")
import sql
from config import base, tabl


@pytest.yield_fixture(autouse=True)
def base_create():
    connect_sql = sqlite3.connect(f"{base}.db", timeout=5)
    curs = connect_sql.cursor()
    curs.execute(f"DELETE FROM {tabl}")
    curs.execute(
        f"""INSERT INTO {tabl}(device_id, device_path, device_reg, date_in, date_out, fio, tabnum, department)
                    VALUES ('name_one','1','1','1',NULL,NULL,NULL,NULL),
                    ('name2','2','2','2','2','2','2','2'),
                    ('3','3','3','3','3',NULL,NULL,NULL),
                    ('4',4,4,4,'four','four',4,'four'),
                    ('5',5,5,5,'five',5,'five','five'),
                    ('six',6,6,6,6,6,6,6);"""
    )
    connect_sql.commit()


en = mimesis.Person("en")
ru = mimesis.Person("ru")
gen = mimesis.Generic("en")
text = mimesis.Text("en")
date = mimesis.Datetime("en")


def test_write_to_database_flash_drive():
    device_id = "7"
    content = text.text()
    regist = text.text()
    date_in = date.datetime()
    curs = sql.open_base()
    assert sql.write_to_database_flash_drive(device_id, content, regist, date_in) == 201
    curs.execute(f"SELECT * FROM {tabl} WHERE device_id='{device_id}'")
    result = curs.fetchall()
    assert result == [
        (
            f"{device_id}",
            f"{content}",
            f"{regist}",
            f"{date_in}",
            None,
            None,
            None,
            None,
        )
    ]


def test_write_to_database_issuing_flash_drive():
    device_id = en.username()
    date_out = date.datetime()
    fio = ru.full_name()
    tabnum = gen.code.imei()
    department = ru.occupation()
    assert (
        sql.write_to_database_issuing_flash_drive(
            device_id, date_out, fio, tabnum, department
        )
        == 404
    )


def test_cleaning_resulting_flash_drive():
    device_id = en.username()
    assert sql.cleaning_resulting_flash_drive(device_id) == 404


def test_cleaning_resulting_flash_drive():
    device_id = "name2"
    curs = sql.open_base()
    assert sql.cleaning_resulting_flash_drive(device_id) == 201
    curs.execute(f"SELECT * FROM {tabl} WHERE device_id='name2'")
    result = curs.fetchall()
    assert result == [(f"name2", "2", "2", 2, None, None, None, None)]


def test_search_flash_drive_based_on_id():
    device_id = en.username()
    result = sql.search_flash_drive_based_on_id(device_id)
    assert result[0] == 404


def test_search_flash_drive_based_on_fio_or_tadnumder():
    fiotab = ru.full_name() or gen.code.imei()
    result = sql.search_flash_drive_based_on_fio_or_tadnumder(fiotab)
    assert result[0] == 404


def test_file_search_based_on_id():
    device_id = en.username()
    result = sql.file_search_based_on_id(device_id)
    assert result[0] == 404


def test_true_write_to_database_issuing_flash_drive():
    date_out = date.datetime()
    fio = ru.full_name()
    tabnum = gen.code.imei()
    department = ru.occupation()
    curs = sql.open_base()
    assert (
        sql.write_to_database_issuing_flash_drive(
            "name_one", date_out, fio, tabnum, department
        )
        == 201
    )
    curs.execute(f"SELECT * FROM {tabl} WHERE device_id='name_one'")
    result = curs.fetchall()
    assert result == [
        (
            f"name_one",
            "1",
            "1",
            1,
            f"{date_out}",
            f"{fio}",
            int(tabnum),
            f"{department}",
        )
    ]


def test_true_search_flash_drive_based_on_id():
    result = sql.search_flash_drive_based_on_id("six")
    assert result[0] == 200


def test_true_search_decommissioned_flash_drives():
    answer = sql.search_decommissioned_flash_drives()
    assert answer[0] == 200


def test_true_file_search_based_on_id():
    device_id = "name_one"
    result = sql.file_search_based_on_id(device_id)
    assert result[0] == 200


def test_true_search_flash_drive_based_on_fio():
    fiotab = "four"
    result = sql.search_flash_drive_based_on_fio_or_tadnumder(fiotab)
    assert result[0] == 200


def test_true_search_flash_drive_based_on_tadnumder():
    fiotab = "five"
    result = sql.search_flash_drive_based_on_fio_or_tadnumder(fiotab)
    assert result[0] == 200
