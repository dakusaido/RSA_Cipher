from sqlalchemy import Column, Integer, String

from utils.DataBase.DataBase import Base


class User(Base):
    __tablename__ = '__Users__'

    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
