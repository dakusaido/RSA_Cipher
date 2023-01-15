import sys
import os
import inspect

from PyQt5 import QtWidgets

# Windows
from windows.MainWindow import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)

    # Windows Initialization
    main_window = MainWindow()

    main_window.show()

    app.exec()


if __name__ == '__main__':
    main()
