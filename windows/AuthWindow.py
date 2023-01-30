import sys

from PyQt5 import QtWidgets
from PyQt5 import QtGui

from qtwidgets import PasswordEdit

from PyQt5.QtCore import QSize, Qt, QThreadPool

from utils.Thread.Worker import Worker
from utils.Auth.Auth import auth
from utils.sql_commands.commands import get_user, register_user

from windows.MainWindow import MainWindow

from config.projectPath.getProjectPath import get_project_path


class AuthWindow(QtWidgets.QWidget):
    __window_title_text = 'AuthWindow'
    __window_size = QSize(400, 200)
    __window_min_size = QSize(300, 150)
    __window_max_size = QSize(400, 200)

    __labelText = '<font size="4"> Auth </font>'
    __buttonText = 'Login'

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.setFixedSize(self.__window_size)
        self.setMinimumSize(self.__window_min_size)
        self.setMaximumSize(self.__window_max_size)
        self.setWindowTitle(self.__window_title_text)

        # Initialization Widgets
        self.label = QtWidgets.QLabel(self.__labelText)
        self.login = QtWidgets.QLineEdit()
        self.password = PasswordEdit()
        self.submit = QtWidgets.QPushButton(self.__buttonText)
        self.dontHaveAccount = QtWidgets.QPushButton("don't have account? Create it..")

        # Settings widgets
        self.label.setAlignment(Qt.AlignCenter)
        self.login.setPlaceholderText('Please enter your username')
        self.password.setPlaceholderText('Please enter your password')
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        # Initialization Blocks
        self.vbox = QtWidgets.QVBoxLayout(self)

        # Setting Blocks
        # Vbox
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.login)
        self.vbox.addWidget(self.password)
        self.vbox.addWidget(self.submit)
        self.vbox.addWidget(self.dontHaveAccount)

        # Connections
        self.submit.clicked.connect(self.submit_action)
        self.dontHaveAccount.clicked.connect(self.dontHaveAccount_action)

        self.threadpool = QThreadPool()

    def submit_action(self):
        if not self.login.displayText():
            self.showMessage(text="Login isn't string")
            return

        if not self.password.displayText():
            self.showMessage(text="Password isn't string")
            return

        return self._submit_action()

    def _submit_action(self):

        worker = Worker(
            fn=auth,
            login=self.login.displayText(),
            password=self.password.text()
        )

        worker.signals.result.connect(self.do_auth)
        worker.signals.finish.connect(self.thread_complete)
        worker.signals.error.connect(self.not_auth)

        self.threadpool.start(worker)

    def dontHaveAccount_action(self):
        pass

    def showMessage(self, text):
        msg = QtWidgets.QMessageBox()

        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.resize(250, 200)

        msg.setText(text)
        # msg.setInformativeText('More information')

        msg.show()
        msg.exec()

    def do_auth(self, bool_):

        if not bool_:
            return

        app = QtWidgets.QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        app.exec()


        self.close()

    def not_auth(self, result):
        self.showMessage(result[1].__str__())

    def thread_complete(self, *args, **kwargs):
        pass
