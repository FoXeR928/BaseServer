import mimesis
import sqlite3
import sql
from config import load_config


cfg = load_config()


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
gen = mimesis.Generic("en")
text = mimesis.Text("en")
date = mimesis.Datetime("en")


def test_base_recording_file():
    device_id = en.username()
    content = text.text()
    regist = text.text()
    date_in = date.datetime()
    assert sql.base_recording_file(device_id, content, regist, date_in)


def test_base_recording_file_device():
    device_id = en.username()
    date_out = date.datetime()
    fio = ru.full_name()
    tabnum = gen.code.imei()
    department = ru.occupation()
    assert sql.base_recording_file_device(device_id, date_out, fio, tabnum, department)


def test_base_clear_device():
    device_id = en.username()
    assert sql.base_clear_device(device_id)


def test_base_check_flask_id():
    device_id = en.username()
    assert sql.base_check_flask_id(device_id)


def base_check_flask_name():
    fiotab = ru.full_name() or gen.code.imei()
    assert sql.base_check_flask_name(fiotab)


def test_base_date_flask():
    device_id = en.username()
    assert sql.base_date_flask(device_id)


def test_true_base_recording_file_device():
    date_out = date.datetime()
    fio = ru.full_name()
    tabnum = gen.code.imei()
    department = ru.occupation()
    assert sql.base_recording_file_device("name_one", date_out, fio, tabnum, department)


def test_true_base_clear_device():
    assert sql.base_check_flask_id("six")==[('six', 6, 6, 6, 6, 6, 6, 6)]

def test_true_true_base_check_flask_off():
    answer = sql.base_check_flask_off()
    assert answer == [("3", 3, 3, 3, 3, None, None, None)]


def test_true_true_base_check_flask_off():
    answer = sql.base_check_flask_off()
    assert answer == [("3", 3, 3, 3, 3, None, None, None)]


def test_base_date_flask():
    device_id = "name_one"
    assert sql.base_date_flask(device_id) == [(1, 1)]


def test_true_base_check_flask_name():
    fiotab = "four"
    assert sql.base_check_flask_name(fiotab) == [
        ("4", 4, 4, 4, "four", "four", 4, "four")
    ]


def test_true_base_check_flask_tabnum():
    fiotab = "five"
    assert sql.base_check_flask_name(fiotab) == [
        ("5", 5, 5, 5, "five", 5, "five", "five")
    ]
