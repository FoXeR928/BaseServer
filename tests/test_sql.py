import mimesis
import sys
import pytest

sys.path.append("./")
import sql
from db_set import tabl


@pytest.yield_fixture(autouse=True)
def base_create():
    session=sql.open_base()
    session.query(tabl).delete()
    record=tabl([device_id='name_one', device_path='1', device_reg='1', date_in='1'),
    (device_id='name2', device_path='2', device_reg='2', date_in='2', date_out='2', fio='2', tabnum='2', department='2'),
    (device_id='3', device_path='3', device_reg='3', date_in='3', date_out='3', fio='3'),
    (device_id='4', device_path='4', device_reg='4', date_in='4', date_out='four', fio='four', tabnum='4', department='four'),
    (device_id='5', device_path='5', device_reg='5', date_in='5', date_out='five', fio='5', tabnum='five', department='five'),
    (device_id='six', device_path='6', device_reg='6', date_in='6', date_out='6', fio='6', tabnum='6', department='6'))
    session.add(record)
    session.commit()



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
    assert sql.write_to_database_flash_drive(device_id, content, regist, date_in) == [201, 'record created']
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
        == [404, 'Not result']
    )


def test_cleaning_resulting_flash_drive():
    device_id = en.username()
    assert sql.cleaning_resulting_flash_drive(device_id) == [404, 'Not found']


def test_cleaning_resulting_flash_drive():
    device_id = "name2"
    curs = sql.open_base()
    assert sql.cleaning_resulting_flash_drive(device_id) == [201, 'record created']
    curs.execute(f"SELECT * FROM {tabl} WHERE device_id='name2'")
    result = curs.fetchall()
    assert result == [(f"name2", "2", "2", 2, None, None, None, None)]


def test_search_flash_drive_based_on_id():
    device_id = en.username()
    result = sql.search_flash_drive_based_on_id(device_id)
    assert result == [404, 'Not found']


def test_search_flash_drive_based_on_fio_or_tadnumder():
    fiotab = ru.full_name() or gen.code.imei()
    result = sql.search_flash_drive_based_on_fio_or_tadnumder(fiotab)
    assert result == [404, 'Not found']


def test_file_search_based_on_id():
    device_id = en.username()
    result = sql.file_search_based_on_id(device_id)
    assert result == [404, 'Not found']


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
        == [201, 'record created']
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
    assert result[0] == [200, 'Status ok']


def test_true_search_decommissioned_flash_drives():
    answer = sql.search_decommissioned_flash_drives()
    assert answer[0] == [200, 'Status ok']


def test_true_file_search_based_on_id():
    device_id = "name_one"
    result = sql.file_search_based_on_id(device_id)
    assert result[0] == [200, 'Status ok']


def test_true_search_flash_drive_based_on_fio():
    fiotab = "four"
    result = sql.search_flash_drive_based_on_fio_or_tadnumder(fiotab)
    assert result[0] == [200, 'Status ok']


def test_true_search_flash_drive_based_on_tadnumder():
    fiotab = "five"
    result = sql.search_flash_drive_based_on_fio_or_tadnumder(fiotab)
    assert result[0] == [200, 'Status ok']
