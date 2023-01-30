from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize

# Windows
# from windows.EncryptWindow import EncryptWindow
# from windows.DecryptWindow import DecryptWindow


class MainWindow(QtWidgets.QWidget):
    # encrypt_button_text = 'Encrypt Data'
    # decrypt_button_text = 'Decrypt Data'
    # use_private_key_text = "Open file with private key"
    # __window_title_text = 'MainWindow'
    #
    # __window_size = QSize(300, 150)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

    #     self.setFixedSize(self.__window_size)
    #     self.setWindowTitle(self.__window_title_text)
    #
    #     # Initialization buttons
    #     self.encrypt_button = QtWidgets.QPushButton(self.encrypt_button_text)
    #     self.decrypt_button = QtWidgets.QPushButton(self.decrypt_button_text)
    #     self.use_private_key_button = QtWidgets.QPushButton(self.use_private_key_text)
    #
    #     # Initialization boxes
    #     self.vbox = QtWidgets.QVBoxLayout(self)
    #
    #     # Boxes actions
    #     self.vbox_action()
    #
    #     # Button connections
    #     self.encrypt_button.clicked.connect(self.on_click_encrypt_button)
    #     self.decrypt_button.clicked.connect(self.on_click_decrypt_button)
    #
    # def vbox_action(self):
    #     self.vbox.addWidget(self.encrypt_button)
    #     self.vbox.addWidget(self.decrypt_button)
    #
    # def on_click_encrypt_button(self):
    #     return self._create_encrypt_window()
    #
    # def on_click_decrypt_button(self):
    #     return self._create_decrypt_window()
    #
    # def _create_encrypt_window(self):
    #     self.encrypt_window = EncryptWindow()
    #     self.encrypt_window.show()
    #
    # def _create_decrypt_window(self):
    #     self.decrypt_window = DecryptWindow()
    #     self.decrypt_window.show()
