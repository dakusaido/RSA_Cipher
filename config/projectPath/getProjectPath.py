from environs import Env


def get_project_path():
    env = Env()
    cur_folder = __file__[:-17]
    env.read_env(cur_folder + 'projectPath.env')
    return env.str('__PROJECT_FOLDER_PATH')
