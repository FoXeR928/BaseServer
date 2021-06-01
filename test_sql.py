import mimesis
import sql

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
