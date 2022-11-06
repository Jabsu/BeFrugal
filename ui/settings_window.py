from PySide6.QtCore import QSize, Qt, Signal

from PySide6.QtWidgets import (QCheckBox, QGridLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
                               QWidget, QComboBox)


class UI_Settings(QWidget):

    close_signal = Signal()
    
    def __init__(self):

        super().__init__()
        self.resize(287, 210)
        self.setMaximumSize(QSize(370, 210))

        main_grid = QGridLayout(self)
        grid_1 = QGridLayout()
        grid_2 = QGridLayout()

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        currency_label = QLabel("Currency (cosmetic)")
        self.currency = QLineEdit()
        self.currency.setSizePolicy(size_policy)
        self.currency.setMaximumSize(QSize(50, 16777215))

        theme_label = QLabel("Theme")

        self.themes = QComboBox()

        grid_1.addWidget(theme_label, 0, 0, 1, 1, Qt.AlignLeft)
        grid_1.addWidget(self.themes, 0, 1, 1, 1, Qt.AlignRight)
        grid_1.addWidget(currency_label, 1, 0, 1, 1, Qt.AlignLeft)
        grid_1.addWidget(self.currency, 1, 1, 1, 1, Qt.AlignRight)

        self.show_fmt_dialog_toggle = QCheckBox()
        self.show_fmt_dialog_toggle.setText(
            "Show formatting dialog after each import")

        horizontal_spacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.delete_history = QPushButton("Delete transaction history")
        self.configure_categories = QPushButton("Configure categories")

        grid_2.addWidget(self.show_fmt_dialog_toggle, 0, 0, 1, 1, Qt.AlignLeft)
        grid_2.addItem(horizontal_spacer, 1, 0, 1, 1)
        grid_2.addWidget(self.delete_history, 2, 0, 1, 1, Qt.AlignLeft)
        grid_2.addWidget(self.configure_categories, 3, 0, 1, 1, Qt.AlignLeft)

        main_grid.addLayout(grid_1, 0, 0, 1, 1)
        main_grid.addLayout(grid_2, 1, 0, 1, 1)

    def closeEvent(self, event):
        self.close_signal.emit()
        event.accept()


    
