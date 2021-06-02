import mimesis
import app

en = mimesis.Person("en")
ru = mimesis.Person("ru")
cod_status = mimesis.Internet("en")
gen = mimesis.Generic("en")
file = mimesis.File("en")


def test_device_id_date():
    cod = cod_status.http_status_code()
    device_id = en.password()
    assert app.date_flask(cod, device_id)

def test_device_id_get():
    cod = cod_status.http_status_code()
    device_id = en.password()
    assert app.get_flask(cod, device_id)

def test_device_id():
    cod = cod_status.http_status_code()
    device_id = en.password()
    assert app.id_flask(cod, device_id)

def test_give_file():
    cod = cod_status.http_status_code()
    device_id = en.password()
    fio = ru.full_name()
    tabnum = gen.code.imei()
    department = ru.occupation()
    assert app.give_file(cod, device_id, fio, tabnum, department)


def test_code_flask_off():
    cod = cod_status.http_status_code()
    assert app.off_flask(cod)

def test_code_flask_all():
    cod = cod_status.http_status_code()
    assert app.all_flask(cod)


def test_name_flask():
    cod = cod_status.http_status_code()
    fiotab = ru.full_name() or gen.code.imei()
    assert app.name_flask(cod, fiotab)
