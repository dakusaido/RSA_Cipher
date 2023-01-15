import os
import sys

from Crypto.PublicKey.RSA import RsaKey
from Crypto.Math.Numbers import Integer

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize, QPoint, QThreadPool

from utils.Thread.Worker import Worker
from utils.RSA.RSACipher import RSACipher
from utils.File.File import File

from config.projectPath.getProjectPath import get_project_path

from environs import Env


class Window(QtWidgets.QWidget):
    project_path = get_project_path()
    window_min_size = QSize(300, 150)
    window_max_size = QSize(400, 200)

    def __init__(self, parent=None, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, parent=parent)

        self.label_text = kwargs.get('label_text')
        self.button_text = kwargs.get('button_text')
        self.save_button_text = kwargs.get('save_button_text')

        self.__env_path = 'config/personKey/personKey.env'
        self.__window_title_text = kwargs.get('window_name')
        self.__crypt_text_variable = kwargs.get('crypt_text_variable')
        self.__crypt_text = ''

        # Initialization Widgets
        self.label = QtWidgets.QLabel(self.label_text)
        self.input_text = QtWidgets.QLineEdit()
        self.input_private_key_len = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton(self.button_text)

        self.save_button = QtWidgets.QPushButton(self.save_button_text)
        self.use_private_key_radio_button = QtWidgets.QRadioButton('Use Person private key')

        # Initialization boxes
        self.vbox = QtWidgets.QVBoxLayout(self)
        self.hbox_text = QtWidgets.QHBoxLayout()
        self.hbox_private_key_len = QtWidgets.QHBoxLayout()

        self.threadpool = QThreadPool()

        self.init_qt()

    def init_qt(self):
        self.setMinimumSize(self.window_min_size)
        self.setMaximumSize(self.window_max_size)
        self.setWindowTitle(self.__window_title_text)

        self.save_button.setEnabled(False)

        # Settings Widgets
        self.label.setAlignment(Qt.AlignCenter)

        # HBoxes actions
        self.hbox_text.addWidget(self.input_text)

        self.hbox_private_key_len.addWidget(self.input_private_key_len)
        self.hbox_private_key_len.addWidget(self.button)

        # Vbox actions
        self.vbox.addWidget(self.label)
        self.vbox.addLayout(self.hbox_text)
        self.vbox.addLayout(self.hbox_private_key_len)
        self.vbox.addWidget(self.save_button)
        self.vbox.addWidget(self.use_private_key_radio_button)

        # Button connections
        self.button.clicked.connect(self.on_click_button)
        self.save_button.clicked.connect(self.save_file)
        self.use_private_key_radio_button.clicked.connect(self.on_click_radio_button)

    def on_click_button(self):
        ...

    def _on_click_button(self):
        ...

    def save_file(self):
        options = QtWidgets.QFileDialog.Options()
        # options |= QtWidgets.QFileDialog.DontUseNativeDialog  # PyQt5 default dialog
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Select path and file name for saving.",
            "",
            "Env Files (*.env)",
            options=options
        )

        if not filename:
            return self.file_not_saved()

        return self._save_file(filename=filename)

    def _save_file(self, filename):
        try:
            with open(file=filename, mode='w', encoding='utf-8') as file:
                file.write(self.__crypt_text_variable + ' = ' + self.__crypted_text)

        except Exception as e:
            print(e)  # Logger
            return self.file_not_saved(exception=e)

        else:
            self.label.setText("Saved!")

    def file_not_saved(self, exception=None):

        if exception:
            ...

        self.label.setText("[ERROR] Not saved")

    def on_click_radio_button(self):
        ...

    def get_person_private_key(self):

        env = Env()
        env_file = self._project_path + self.__env_path
        env.read_env(env_file)

        components = ['n', 'e', 'd', 'p', 'q', 'u']

        if not os.path.exists(env_file):
            rsa = RSACipher()
            key_len = 1024
            rsa.generate_key(key_len)
            rsa.save_private_key(env_file)
            return rsa.key

        params = [Integer(int(env.str(component))) for component in components]

        n = params[0]
        e = params[1]
        d = params[2]
        p = params[3]
        q = params[4]
        u = params[5]

        return RsaKey(n=n, e=e, d=d, p=p, q=q, u=u)

    def __save_crypt_text(self, a0: str):
        self.__crypt_text = a0

    def thread_complete(self, *args, **kwargs):
        self.button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.label.setText("Encrypted!")

    def line_text_is_none(self):
        self.label.setText("Text is None")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window(**{'label_text':'blabla'})
    window.show()
    app.exec()
