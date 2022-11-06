from PySide6.QtCore import QSize, Qt, Signal

from PySide6.QtWidgets import (QGridLayout, QLabel, QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
                               QWidget, QLineEdit)


class UI_ConfigCategories(QWidget):

    close_signal = Signal()

    def __init__(self):
        super().__init__()
        self.resize(820, 350)
        self.setWindowTitle("Configure categories")
        
        self.grid_layout = QGridLayout(self)

        horizontal_spacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        
        payers = QLabel('<span style="font-weight:bold">Payers</span>')
        recipients = QLabel('<span style="font-weight:bold">Recipients</span>')

        self.grid_layout.addWidget(payers, 0, 0, 1, 1, Qt.AlignHCenter)
        self.grid_layout.addWidget(recipients, 0, 1, 1, 1, Qt.AlignHCenter)

        # Buttons
        self.continue_button = QPushButton()

        # Scroll area (payers)
        self.scroll_area_L = QScrollArea(self)
        self.scroll_area_L.setWidgetResizable(True)
        self.scroll_area_L_contents = QWidget()
        self.scroll_area_L.setWidget(self.scroll_area_L_contents)
        self.grid_L = QGridLayout(self.scroll_area_L_contents)
        
        # Scroll area (recipients)
        self.scroll_area_R = QScrollArea(self)
        self.scroll_area_R.setWidgetResizable(True)
        self.scroll_area_R_contents = QWidget()
        self.scroll_area_R.setWidget(self.scroll_area_R_contents)
        self.grid_R = QGridLayout(self.scroll_area_R_contents)

        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)

        
        
        for var_name in ['grid_L', 'grid_R']:
            entity_header = QLabel("Ent")
            occurrence_header = QLabel("occ")
            category_header = QLabel("cat")
            entity_header.setSizePolicy(size_policy)

            entity_header.setText("<span style=\"font-weight:bold\">Entity</span>")
            occurrence_header.setText("<span style=\"font-weight:bold\">#</span>")
            occurrence_header.setToolTip("Number of occurrences")
            category_header.setText("<span style=\"font-weight:bold\">Category</span>")
        
            getattr(self, var_name).addWidget(entity_header, 0, 0, 1, 1)
            getattr(self, var_name).addWidget(occurrence_header, 0, 1, 1, 1)
            getattr(self, var_name).addWidget(category_header, 0, 2, 1, 1)
        
        self.grid_layout.addWidget(self.scroll_area_L, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.scroll_area_R, 1, 1, 1, 1)
        
        # Last grid
        self.grid_layout_3 = QGridLayout()
        label = QLabel("Create a new category:")
        self.new_category = QLineEdit()
        self.add_category_button = QPushButton("➕")
        self.add_category_button.setMaximumSize(QSize(30, 16777215))
        self.grid_layout.addLayout(self.grid_layout_3, 7, 0, 1, 1)
        self.grid_layout_3.addItem(horizontal_spacer, 6, 0, 1, 1)
        self.grid_layout_3.addWidget(label, 7, 0, 1, 1)
        self.grid_layout_3.addWidget(self.new_category, 7, 1, 1, 1)
        self.grid_layout_3.addWidget(self.add_category_button, 7, 2, 1, 1)
        self.grid_layout_3.addItem(horizontal_spacer, 7, 3, 1, 1)
        
        self.category_added = QLabel("")
        self.grid_layout.addWidget(self.category_added, 8, 0, 1, 1)

    def closeEvent(self, event):
        self.close_signal.emit()
        event.accept()



        