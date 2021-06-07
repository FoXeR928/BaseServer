from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

base = declarative_base()
engine = create_engine("sqlite:///flask-date.db")

base.metadata.create_all(engine)


class tabl(base):
    __tablename__ = "flasks"

    id=Column(Integer, nullable=False, unique=True, primary_key=True)
    device_id = Column(String)
    device_path = Column(String)
    device_reg = Column(String)
    date_in = Column(Integer)
    date_out = Column(Integer)
    fio = Column(String)
    tabnum = Column(Integer)
    department = Column(String)
