import mimesis
import sqlite3
import sys
import pytest
from sqlalchemy.orm import session

sys.path.append("./")
import sql
from config import base, tabl
from db_set import Base, Tabl


list_len = 6
err = 1
not_err = 0


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
gen = mimesis.Generic("en")
text = mimesis.Text("en")
date = mimesis.Datetime("en")


def test_write_to_database_flash_drive():
    device_id = "7"
    content = "text veryyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy looooooooooooooooooooooooooooooooooong text"
    regist = "text veryyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy looooooooooooooooooooooooooooooooooong text2222222222222222222222222222222222222222222222222222"
    date_in = date.datetime()
    session = sql.open_base(Base)
    result = sql.write_to_database_flash_drive(
        Tabl, device_id, content, regist, date_in
    )
    assert result["err"] == not_err
    session.query(tabl).filter(tabl.device_id == device_id).all()
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


def test_false_write_to_database_flash_drive():
    device_id = "name_one"
    content = "text veryyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy looooooooooooooooooooooooooooooooooong text"
    regist = "text veryyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy looooooooooooooooooooooooooooooooooong text2222222222222222222222222222222222222222222222222222"
    date_in = date.datetime()
    session = sql.open_base(Base)
    result = sql.write_to_database_flash_drive(
        Tabl, device_id, content, regist, date_in
    )
    assert result["err"] == err
    result = session.query(tabl).all()
    assert len(result) == list_len


def test_write_to_database_issuing_flash_drive():
    device_id = "7"
    date_out = date.datetime()
    fio = ru.full_name()
    tabnum = gen.code.imei()
    department = ru.occupation()
    curs = sql.open_base(Base)
    result = sql.write_to_database_issuing_flash_drive(
        Tabl, device_id, date_out, fio, tabnum, department
    )
    assert result["err"] == not_err
    curs.execute(f"SELECT * FROM {tabl}")
    result = curs.fetchall()
    assert len(result) == list_len


def test_cleaning_resulting_flash_drive():
    device_id = "7"
    result = sql.cleaning_resulting_flash_drive(Tabl, device_id)
    assert result["err"] == not_err


def test_true_cleaning_resulting_flash_drive():
    device_id = "name2"
    curs = sql.open_base(Base)
    result = sql.cleaning_resulting_flash_drive(Tabl, device_id)
    assert result["err"] == not_err
    curs.execute(f"SELECT * FROM {Tabl} WHERE device_id='name2'")
    result = curs.fetchall()
    assert result == [
        (
            f"name2",
            "text_txt",
            "text_reg",
            "2011-10-13 16:23:16.083572",
            None,
            None,
            None,
            None,
        )
    ]


def test_search_flash_drive_based_on_id():
    device_id = "7"
    result = sql.search_flash_drive_based_on_id(Tabl, device_id)
    assert result["err"] == err


def test_search_flash_drive_based_on_fio():
    fio = "It is name"
    result = sql.search_flash_drive_based_on_fio(Tabl, fio)
    assert result["err"] == err


def test_search_flash_drive_based_on_tabnum():
    tabnum = "4654646464646464444444444444444444444444444444"
    result = sql.search_flash_drive_based_on_tadnum(Tabl, tabnum)
    assert result["err"] == err


def test_file_search_based_on_id():
    device_id = "7"
    result = sql.file_search_based_on_id(Tabl, device_id)
    assert result["err"] == err


def test_true_write_to_database_issuing_flash_drive():
    date_out = date.datetime()
    fio = ru.full_name()
    tabnum = gen.code.imei()
    department = ru.occupation()
    curs = sql.open_base(Base)
    result = sql.write_to_database_issuing_flash_drive(
        Tabl, "name_one", date_out, fio, tabnum, department
    )
    assert result["err"] == not_err
    curs.execute(f"SELECT * FROM {base} WHERE device_id='name_one'")
    result = curs.fetchall()
    assert result == [
        (
            f"name_one",
            "text_txt",
            "text_reg",
            "2011-10-13 16:23:16.083572",
            f"{date_out}",
            f"{fio}",
            int(tabnum),
            f"{department}",
        )
    ]


def test_true_search_flash_drive_based_on_id():
    result = sql.search_flash_drive_based_on_id(Tabl, "name6")
    assert result["err"] == not_err


def test_true_search_decommissioned_flash_drives():
    answer = sql.search_decommissioned_flash_drives(Tabl)
    assert answer["err"] == not_err


def test_true_file_search_based_on_id():
    device_id = "name_one"
    result = sql.file_search_based_on_id(Tabl, device_id)
    assert result["err"] == not_err


def test_true_search_flash_drive_based_on_fio():
    fio = "Велигор Миссюров"
    result = sql.search_flash_drive_based_on_fio(Tabl, fio)
    assert result["err"] == not_err


def test_true_search_flash_drive_based_on_tadnumder():
    tabnum = 358240054017520
    result = sql.search_flash_drive_based_on_tadnum(Tabl, tabnum)
    assert result["err"] == not_err


def test_true_result_search_flash_drive_based_on_id():
    result = sql.search_flash_drive_based_on_id(Tabl, "name6")
    assert result["result"] == [
        (
            "name6",
            "text_txt",
            "text_reg",
            "2011-10-13 16:23:16.083572",
            "2019-03-07 23:17:50.848051",
            "Ынтымак Горляков",
            358240054017520,
            "Кассир",
        )
    ]


def test_true_result_search_decommissioned_flash_drives():
    answer = sql.search_decommissioned_flash_drives(Tabl)
    assert answer["result"] == [
        (
            "name3",
            "text_txt",
            "text_reg",
            "2011-10-13 16:23:16.083572",
            "2019-03-07 23:17:50.848051",
            None,
            None,
            None,
        ),
    ]


def test_true_result_file_search_based_on_id():
    device_id = "name_one"
    result = sql.file_search_based_on_id(Tabl, device_id)
    assert result["result"] == [("text_txt", "text_reg")]


def test_true_result_search_flash_drive_based_on_fio():
    fio = "Велигор Миссюров"
    result = sql.search_flash_drive_based_on_fio(Tabl, fio)
    assert result["result"] == [
        (
            "name4",
            "text_txt",
            "text_reg",
            "2011-10-13 16:23:16.083572",
            "2019-03-07 23:17:50.848051",
            "Велигор Миссюров",
            353166055808564,
            "Травматолог",
        )
    ]


def test_true_result_search_flash_drive_based_on_tadnumder():
    tabnum = 358240054017520
    result = sql.search_flash_drive_based_on_tadnum(Tabl, tabnum)
    assert result["result"] == [
        (
            "name6",
            "text_txt",
            "text_reg",
            "2011-10-13 16:23:16.083572",
            "2019-03-07 23:17:50.848051",
            "Ынтымак Горляков",
            358240054017520,
            "Кассир",
        )
    ]
