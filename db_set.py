from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config import base, tabl_name

Base = declarative_base()
engine = create_engine(f"sqlite:///{base}.db")

Base.metadata.create_all(engine)


class Tabl(Base):
    __tablename__ = tabl_name

    device_id = Column(String, nullable=False, unique=True, primary_key=True)
    device_path = Column(String, nullable=False)
    device_reg = Column(String, nullable=False)
    date_in = Column(Integer, nullable=False)
    date_out = Column(Integer)
    fio = Column(String)
    tabnum = Column(Integer)
    department = Column(String)
