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
    device_id = en.username()
    content = text.text()
    regist = text.text()
    date_in = date.datetime()
    assert sql.write_to_database_flash_drive(device_id, content, regist, date_in) == 201


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


def test_search_flash_drive_based_on_id():
    device_id = en.username()
    assert sql.search_flash_drive_based_on_id(device_id) == 404


def test_search_flash_drive_based_on_fio_or_tadnumder():
    fiotab = ru.full_name() or gen.code.imei()
    assert sql.search_flash_drive_based_on_fio_or_tadnumder(fiotab) == 404


def test_file_search_based_on_id():
    device_id = en.username()
    assert sql.file_search_based_on_id(device_id) == 404


def test_true_write_to_database_issuing_flash_drive():
    date_out = date.datetime()
    fio = ru.full_name()
    tabnum = gen.code.imei()
    department = ru.occupation()
    assert (
        sql.write_to_database_issuing_flash_drive(
            "name_one", date_out, fio, tabnum, department
        )
        == "Флешка выдана"
    )


def test_true_search_flash_drive_based_on_id():
    assert sql.search_flash_drive_based_on_id("six") == [
        ("six", "6", "6", 6, 6, "6", 6, "6")
    ]


def test_true_search_decommissioned_flash_drives():
    answer = sql.search_decommissioned_flash_drives()
    assert answer == [("3", "3", "3", 3, 3, None, None, None)]


def test_true_file_search_based_on_id():
    device_id = "name_one"
    assert sql.file_search_based_on_id(device_id) == [("1", "1")]


def test_true_search_flash_drive_based_on_fio():
    fiotab = "four"
    assert sql.search_flash_drive_based_on_fio_or_tadnumder(fiotab) == [
        ("4", "4", "4", 4, "four", "four", 4, "four")
    ]


def test_true_search_flash_drive_based_on_tadnumder():
    fiotab = "five"
    assert sql.search_flash_drive_based_on_fio_or_tadnumder(fiotab) == [
        ("5", "5", "5", 5, "five", "5", "five", "five")
    ]
