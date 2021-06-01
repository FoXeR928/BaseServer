import mimesis
from mimesis.locales import NO
from mimesis.providers.code import Code
import sql

en = mimesis.Person("en")
ru = mimesis.Person("ru")
gen = mimesis.Generic("en")


def test_base_recording_file():
    device_id = en.password
    content = mimesis.Text("en").text
    regist = mimesis.Text("en").text
    date_in = mimesis.Datetime.datetime
    assert sql.base_recording_file(device_id, content, regist, date_in)


def test_base_recording_file_device():
    device_id = en.password()
    date_out = 1
    fio = ru.full_name()
    tabnum = gen.code.imei()
    department = ru.occupation()
    assert sql.base_recording_file_device(device_id, date_out, fio, tabnum, department)


def test_base_clear_device():
    device_id = en.password()
    assert sql.base_clear_device(device_id)


def test_base_check_flask_id():
    device_id = en.password()
    assert sql.base_check_flask_id(device_id)


def base_check_flask_name():
    fiotab = ru.full_name() or gen.code.imei()
    assert sql.base_check_flask_name(fiotab)


def test_base_date_flask():
    device_id = en.password()
    assert sql.base_date_flask(device_id)
