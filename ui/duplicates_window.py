from PySide6.QtCore import Qt

from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QAbstractItemView,  QGridLayout, QLabel,
                               QListWidget, QPushButton, QSizePolicy,
                               QSpacerItem, QWidget)


class UI_Duplicates(QWidget):

    def __init__(self):
        super().__init__()

        self.resize(400, 300)
        self.setWindowTitle("Possible duplicates found")

        horizontal_spacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        grid_layout = QGridLayout()

        self.duplicates_found_label = QLabel()
        self.duplicates_found_label.setWordWrap(True)
        grid_layout.addWidget(self.duplicates_found_label,
                              0, 0, 1, 1, Qt.AlignTop)

        font = QFont("Monospace")
        font.setStyleHint(QFont.TypeWriter)
        self.duplicate_list = QListWidget(self)
        self.duplicate_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.duplicate_list.setFont(font)

        self.model = self.duplicate_list.model()
        # self.duplicate_list.setModel(model)
        # self.sel_view = self.duplicate_list.selectionModel()

        # self.duplicate_list.setSelectionModel(model)
        # self.duplicate_list

        grid_layout.addWidget(self.duplicate_list, 3, 0, 1, 1)
        label2 = QLabel()
        label2.setText(
            'Select the transactions you want to KEEP (i.e. saved as unique entries):')
        # label2.setWordWrap(True)
        grid_layout.addWidget(label2, 2, 0, 1, 1)
        grid_layout.addItem(horizontal_spacer, 1, 0, 1, 1)

        grid_layout_2 = QGridLayout(self)
        grid_layout_2.addLayout(grid_layout, 0, 0, 1, 1)
        self.continue_button = QPushButton()
        self.continue_button.setText("Continue")
        grid_layout_2.addWidget(self.continue_button,
                                4, 0, 1, 1, Qt.AlignRight)
        grid_layout_2.addItem(horizontal_spacer, 3, 0, 1, 1)

        grid_layout_3 = QGridLayout()
        self.select_all_button = QPushButton()
        self.select_all_button.setText("Keep all")
        self.deselect_all_button = QPushButton()
        self.deselect_all_button.setText("Ignore all")
        self.deselect_all_button.setEnabled(False)
        grid_layout_3.addItem(horizontal_spacer, 0, 0, 1, 1)
        grid_layout_3.addWidget(self.select_all_button,
                                0, 2, 1, 1, Qt.AlignRight)
        grid_layout_3.addWidget(self.deselect_all_button,
                                0, 1, 1, 1, Qt.AlignRight)
        grid_layout_2.addLayout(grid_layout_3, 1, 0, 1, 1)
