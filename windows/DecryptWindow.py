from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, QPoint, Qt


class DecryptWindow(QtWidgets.QWidget):
    label_text = 'Input Cipher'
    decrypt_button_text = 'Decrypt'

    __window_title_text = 'DecryptWindow'

    __window_min_size = QSize(300, 150)
    __window_max_size = QSize(400, 200)
    __window_position = QPoint(1200, 450)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)

        self.move(self.__window_position)
        self.setWindowTitle(self.__window_title_text)
        self.setMinimumSize(self.__window_min_size)
        self.setMaximumSize(self.__window_max_size)

        # Initialization Widgets
        self.label = QtWidgets.QLabel(self.label_text)
        self.input_encrypted_text = QtWidgets.QLineEdit()
        self.decrypt_button = QtWidgets.QPushButton(self.decrypt_button_text)

        self.save_button = QtWidgets.QPushButton('Save decrypted text')
        self.save_button.setEnabled(False)

        self.use_private_key_radio_button = QtWidgets.QRadioButton('Use Person private key')

        # Settings Widgets
        self.label.setAlignment(Qt.AlignCenter)

        # Initialization boxes
        self.vbox = QtWidgets.QVBoxLayout(self)
        self.hbox_text = QtWidgets.QHBoxLayout()

        # Vbox actions
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.input_encrypted_text)
        self.vbox.addWidget(self.decrypt_button)
        self.vbox.addWidget(self.save_button)
        self.vbox.addWidget(self.use_private_key_radio_button)


