from sqlalchemy import Column, Integer, String

from utils.DataBase.DataBase import Base


class User(Base):
    __tablename__ = '__passwords__'

    id = Column(Integer, primary_key=True, unique=True)
    n = Column(String, nullable=False)
    e = Column(String, nullable=False)
    d = Column(String, nullable=False)
    p = Column(String, nullable=False)
    q = Column(String, nullable=False)
    u = Column(String, nullable=False)
