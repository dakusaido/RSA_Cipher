import sys
import os
import inspect

from PyQt5 import QtWidgets

from utils.DataBase.DataBase import create_base

# Windows
from windows.AuthWindow import AuthWindow


def main():
    app = QtWidgets.QApplication(sys.argv)

    # Windows Initialization
    main_window = AuthWindow()
    create_base()

    main_window.show()

    app.exec()


if __name__ == '__main__':
    main()
