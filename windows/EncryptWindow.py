import time
import os

from Crypto.PublicKey.RSA import RsaKey
from Crypto.Math.Numbers import Integer

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize, QPoint, QThreadPool

from utils.Thread.Worker import Worker
from utils.RSA.RSACipher import RSACipher
from utils.File.File import File

from config.projectPath.getProjectPath import get_project_path

from environs import Env


class EncryptWindow(QtWidgets.QWidget):
    label_text = 'Input Data'
    button_text = 'Encrypt'
    __window_title_text = 'EncryptWindow'
    __encrypted_text = ''
    __encrypted_text_variable = 'ENCRYPTED_TEXT'
    __env_path = 'config/personKey/personKey.env'

    _project_path = get_project_path()
    __window_min_size = QSize(300, 150)
    __window_max_size = QSize(400, 200)
    __window_position = QPoint(400, 450)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)

        self.move(self.__window_position)
        self.setMinimumSize(self.__window_min_size)
        self.setMaximumSize(self.__window_max_size)
        self.setWindowTitle(self.__window_title_text)

        # Initialization Widgets
        self.label = QtWidgets.QLabel(self.label_text)
        self.input_text = QtWidgets.QLineEdit()
        self.input_private_key_len = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton(self.button_text)

        self.save_button = QtWidgets.QPushButton('Save encrypted text')
        self.save_button.setEnabled(False)

        self.use_private_key_radio_button = QtWidgets.QRadioButton('Use Person private key')

        # Settings Widgets
        self.label.setAlignment(Qt.AlignCenter)

        # Initialization boxes
        self.vbox = QtWidgets.QVBoxLayout(self)
        self.hbox_text = QtWidgets.QHBoxLayout()
        self.hbox_private_key_len = QtWidgets.QHBoxLayout()

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

        self.threadpool = QThreadPool()

    def on_click_button(self):

        self.button.setEnabled(False)

        rsa = None

        try:
            line_text = self.input_text.displayText()
            private_key_len = self.input_private_key_len.displayText()

        except Exception as e:
            print(e)
            return

        if not line_text:
            return self.line_text_is_none()

        if not private_key_len.isdigit():
            return self.private_key_len_is_not_digit()

        if self.use_private_key_radio_button.isChecked():
            rsa = self.get_person_private_key()

        return self._on_click_button(line_text=line_text, private_key_len=int(private_key_len), rsa=rsa)

    def _on_click_button(self, line_text, private_key_len, rsa=None):

        worker = Worker(
            self.generate_key,
            encrypt_key=line_text,
            private_key_len=private_key_len,
            rsa=rsa
        )

        worker.signals.result.connect(self.__save_encrypted_text)
        worker.signals.finish.connect(self.thread_complete)
        # worker.signals.progress.connect(self.progress_fn)

        self.threadpool.start(worker)

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
                file.write(self.__encrypted_text_variable + ' = ' + self.__encrypted_text)

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

    @staticmethod
    def generate_key(encrypt_key, private_key_len, rsa=None, **kwargs):

        rsa_ = RSACipher(rsa)
        if not rsa:
            rsa_.generate_key(private_key_len)
        encrypted_text = rsa_.encrypt(encrypt_key)

        return encrypted_text

    def get_person_private_key(self):

        env = Env()
        env_file = self._project_path + self.__env_path
        env.read_env(env_file)

        components = ['n', 'e', 'd', 'p', 'q', 'u']

        if not os.path.exists(env_file):
            rsa = RSACipher()
            key_len = self.input_private_key_len.displayText()
            key_len = int(key_len) if key_len.isdigit() else 1024
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

    def __save_encrypted_text(self, a0: str):
        self.__encrypted_text = a0

    def thread_complete(self, *args, **kwargs):
        self.button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.label.setText("Encrypted!")

    def line_text_is_none(self):
        self.label.setText("Text is None")

    def private_key_len_is_not_digit(self):
        self.label.setText("private key length should be integer")
