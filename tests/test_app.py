import mimesis
import sqlite3
import sys
sys.path.append('./')
import app
from fastapi.testclient import TestClient
from config import load_config

file, file_name = sys.argv
conf = open("config.txt", "w+")
conf.write(file_name)
conf.close()

cfg = load_config()

test_client=TestClient(app.app)

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
cod_status = mimesis.Internet("en")
gen = mimesis.Generic("en")
file = mimesis.File("en")


def test_device_id_date():
    responses= test_client.get("/date_flask", json={'device_id':'1'})
    assert responses.status_code==422
    assert responses.json()=={"Флешка":'"Такого в базе нету"'}


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
