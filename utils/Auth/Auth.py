from utils.sql_commands.commands import get_user
from utils.Exceptions.UserNotFoundException import UserNotFound


def auth(login, password, progress_callback=None):
    user = get_user(login)

    if not user:
        raise UserNotFound(f'User not found like {login}')

    if user.password != password:
        raise UserNotFound(f'User {login} not found with password')

    return True


