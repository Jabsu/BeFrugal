from PySide6.QtCore import QSize, Qt

from PySide6.QtWidgets import (QGridLayout, QLabel, QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
                               QWidget, QLineEdit)


class UI_NewEntities(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(520, 335)
        self.setWindowTitle("New entities found")
        
        self.grid_layout = QGridLayout(self)

        horizontal_spacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        # Parent grid labels
        self.entities_found = QLabel()
        additional_text = QLabel()
        additional_text.setWordWrap(True)
        
        # Buttons
        self.continue_button = QPushButton()

        # Scroll area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_contents = QWidget()
        # self.scroll_area_contents.setGeometry(QRect(0, 0, 500, 189))
        self.scroll_area.setWidget(self.scroll_area_contents)
        self.grid_layout_2 = QGridLayout(self.scroll_area_contents)
        
        # Scroll area labels
        entity_header = QLabel(self.scroll_area_contents)
        type_header = QLabel(self.scroll_area_contents)
        category_header = QLabel(self.scroll_area_contents)
        occurrence_header = QLabel(self.scroll_area_contents)

        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(entity_header.sizePolicy().hasHeightForWidth())
        entity_header.setSizePolicy(sizePolicy1)

        # Add items to scroll area grid
        self.grid_layout_2.addWidget(entity_header, 0, 0, 1, 1)
        self.grid_layout_2.addWidget(occurrence_header, 0, 1, 1, 1)
        self.grid_layout_2.addWidget(type_header, 0, 2, 1, 1)
        self.grid_layout_2.addWidget(category_header, 0, 3, 1, 1)
        self.grid_layout_2.addItem(horizontal_spacer, 0, 4, 1, 1)

        # Add items to parent grid
        self.grid_layout.addWidget(self.entities_found, 0, 0, 1, 1, Qt.AlignTop)
        self.grid_layout.addWidget(additional_text, 1, 0, 1, 1, Qt.AlignTop)
        self.grid_layout.addItem(horizontal_spacer, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.scroll_area, 5, 0, 1, 1)
        self.grid_layout.addItem(horizontal_spacer, 6, 0, 1, 1)
        self.grid_layout.addWidget(self.continue_button, 9, 0, 1, 1, Qt.AlignRight)

        # Last grid
        self.grid_layout_3 = QGridLayout()
        label = QLabel("Create a new category:")
        self.new_category = QLineEdit()
        self.add_category_button = QPushButton("➕")
        self.add_category_button.setMaximumSize(QSize(30, 16777215))
        self.grid_layout.addLayout(self.grid_layout_3, 7, 0, 1, 1)
        self.grid_layout_3.addWidget(label, 7, 0, 1, 1)
        self.grid_layout_3.addWidget(self.new_category, 7, 1, 1, 1)
        self.grid_layout_3.addWidget(self.add_category_button, 7, 2, 1, 1)
        self.grid_layout_3.addItem(horizontal_spacer, 7, 3, 1, 1)
        
        self.category_added = QLabel("")
        self.grid_layout.addWidget(self.category_added, 8, 0, 1, 1)

        # Set texts
        additional_text.setText(
            "If you wish, you can leave these as they are (uncategorized) and configure them later.")
        entity_header.setText("<span style=\"font-weight:bold\">Entity</span>")
        occurrence_header.setText("<span style=\"font-weight:bold\">#</span>")
        occurrence_header.setToolTip("Number of occurrences")
        type_header.setText("<span style=\"font-weight:bold\">Type</span>")
        category_header.setText("<span style=\"font-weight:bold\">Category</span>")
        self.continue_button.setText("Continue")



        