from PySide6.QtCore import QSize, Qt

from PySide6.QtWidgets import (QCheckBox, QGridLayout, QLabel,
                               QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
                               QSpinBox, QTextEdit, QVBoxLayout, QWidget, QComboBox)


class UI_Settings(QWidget):

    def __init__(self):

        super().__init__()
        self.resize(287, 210)
        self.setMaximumSize(QSize(370, 210))

        self.grid_1 = QGridLayout()
        self.grid_2 = QGridLayout(self)

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        currency_label = QLabel()

        self.currency = QLineEdit()
        self.currency.setSizePolicy(size_policy)
        self.currency.setMaximumSize(QSize(50, 16777215))

        self.theme = QComboBox()


