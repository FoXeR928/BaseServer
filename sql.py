from logging import info
from os import name
import sqlite3
import logs
from loguru import logger

logs.init_log()

try:
    connect_sql= sqlite3.connect('bd.db')
    curs=connect_sql.cursor()
    logger.debug('Base connect')
except:
    logger.error('Base not connect')

def base_id_check():
    curs.execute("""SELECT id_name from testBD""")
    return(curs.fetchall())

def base_name_check():
    curs.execute("""SELECT name from testBD""")
    return(curs.fetchall())

def base_id():    
    for x in base_id_check():
        return x

def base_name():    
    for x in base_name_check():
        return x