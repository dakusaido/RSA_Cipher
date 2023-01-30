from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc

from utils.DataBase.DataBase import session
from utils.DataBase.struct_data import User


def register_user(username: str, password: str):
    session.connection()
    user = User(
        username=username,
        password=password
    )
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()


def get_user(login):
    try:
        user = session.query(User).filter(
            User.username.like(login)
        ).all()[0]
        return user
    except Exception as e:
        session.rollback()
        return None
