import os
import sys
import inspect
import time


def create_venv(python_exe_path_, proj_path):
    command = ' -m venv '
    os.system(python_exe_path_ + command + proj_path + '.venv')
    time.sleep(20)


def import_requirements(proj_path):
    python_interpreter = proj_path + r'.venv\Scripts\python.exe'
    requirements_path = proj_path + r'requirements.txt'
    os.system(python_interpreter + ' -m pip install -r ' + requirements_path)


def set_project_path(project_path):
    with open(project_path + r'config\projectPath\projectPath.env', mode='w', encoding='utf-8') as file:
        file.write(f'__PROJECT_FOLDER_PATH\t=\t{project_path}')


if __name__ == '__main__':
    project_path = os.path.abspath(inspect.getsourcefile(lambda: 0))[:-6]
    python_env = r'config\PythonInterpreterPath\pythonInterpPath.env'

    set_project_path(project_path)

    if not os.path.exists(project_path + python_env):
        python_exe_path = input(
            r'python.exe Path (For example: C:\Users\...\AppData\Local\Programs\Python\Python38\python.exe)> ')

        with open(project_path + python_env, mode='w', encoding='utf-8') as file:
            file.write("PYTHONPATH = " + python_exe_path)

    else:
        with open(project_path + python_env, mode='r', encoding='utf-8') as file:
            python_exe_path = file.readline().split()[-1]

    if not os.path.exists(project_path + '.venv'):
        create_venv(python_exe_path, project_path)
        import_requirements(project_path)

    os.system(project_path + r'.venv\Scripts\python.exe ' + project_path + r'main.py')
