from PySide6.QtCore import QSize, Qt

from PySide6.QtWidgets import (QCheckBox, QGridLayout, QLabel,
                               QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
                               QSpinBox, QTextEdit, QVBoxLayout, QWidget, QComboBox)


class UI_Formatting(QWidget):

    def __init__(self):

        super().__init__()
        self.resize(644, 283)

        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        # size_policy.setMaximumSize(QSize(16777215, 350))
        # size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMaximumSize(QSize(16777215, 350))
        self.setWindowTitle("Formatting settings")

        self.grid_layout = QGridLayout(self)
        horizontal_spacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.grid_layout.addItem(horizontal_spacer, 7, 0, 1, 6)

        # sample box
        vertical_layout = QVBoxLayout()
        self.sample = QTextEdit()
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(
            self.sample.sizePolicy().hasHeightForWidth())
        self.sample.setSizePolicy(sizePolicy3)
        self.sample.setMaximumSize(QSize(16777215, 50))
        #  self.sample.setLineWrapMode(QTextEdit.NoWrap)
        self.sample.setReadOnly(True)
        vertical_layout.addWidget(self.sample)

        self.grid_layout.addLayout(vertical_layout, 0, 0, 1, 7)

        self.d_span = '<span style="background-color:#FFC228">'
        self.a_span = '<span style="background-color:#FCFF28">'
        self.e_span = '<span style="background-color:#BBFF8D">'
        self.warning = '<span style="color:red">'

        size_policy_2 = QSizePolicy(
            QSizePolicy.Maximum, QSizePolicy.Maximum)
        size_policy_2.setHorizontalStretch(0)
        size_policy_2.setVerticalStretch(0)

        
        # Validity labels
        self.separator_validity = QLabel()
        self.separator_validity.setText(" ")
        self.separator_validity.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.grid_layout.addWidget(self.separator_validity, 4, 2, 1, 1)

        self.date_idx_validity = QLabel()
        self.grid_layout.addWidget(self.date_idx_validity, 5, 2, 1, 1)

        self.amount_idx_validity = QLabel()
        self.grid_layout.addWidget(self.amount_idx_validity, 6, 2, 1, 1)
        
        self.entity_idx_validity = QLabel()
        self.grid_layout.addWidget(self.entity_idx_validity, 7, 2, 1, 1)

        self.date_format_validity = QLabel()
        # self.date_format_validity.setText(" ")
        # self.invalid_format_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        
        
        
        #self.invalid_format_label.setText(
        #    f'{self.warning}No match!</span>')
        # self.invalid_format_label.setSizePolicy(size_policy)

        self.grid_layout.addWidget(self.date_format_validity, 8, 2, 1, 1)
        # self.invalid_format_label.hide()

        widget_pairs = {
            'Configuration preset': 'cfg_preset',
            'Value separator': 'separator',
            f'Transaction {self.d_span}date</span> index': 'date_spinbox',
            f'Transaction {self.a_span}amount</span> index': 'amount_spinbox',
            f'Transaction {self.e_span}entity</span> index': 'entity_spinbox',
            'Date formatting': 'date_format'
        }

        row = 3

        # Create repeating UI elements and self attributes
        for label_text, var_name in widget_pairs.items():

            label = QLabel()
            label.setText(label_text)
            label.setSizePolicy(size_policy_2)
            self.grid_layout.addWidget(label, row, 0, 1, 1)

            var = setattr(self, var_name, object)

            if label_text == 'Value separator':
                var = QLineEdit()
                var.setMaximumSize(QSize(32, 16777215))
                label = QLabel()
                label.setText('%t = tab')
                self.grid_layout.addWidget(label, row, 3, 1, 1)
            elif label_text == 'Configuration preset':
                var = QComboBox()
                var.addItem("Preset 1")
                var.addItem("Preset 2")
                var.addItem("Preset 3")
                
            elif label_text == 'Date formatting':
                var = QLineEdit()
                var.setMinimumSize(QSize(100, 16777215))
                var.setMaximumSize(QSize(100, 16777215))
                var.setPlaceholderText("e.g. %Y/%m/%d")
                label = QLabel()
                label.setText(
                    '<a href="https://strftime.org/">Format codes</a>')
                label.setOpenExternalLinks(True)
                self.grid_layout.addWidget(label, row, 3, 1, 1)
            else:
                var = QSpinBox()
                var.setLayoutDirection(Qt.LeftToRight)

            size_policy_2.setHeightForWidth(
                var.sizePolicy().hasHeightForWidth())

            var.setSizePolicy(size_policy_2)

            setattr(self, var_name, var)
            self.grid_layout.addWidget(getattr(self, var_name), row, 1, 1, 1)

            row += 1

        self.cancel_button = QPushButton()
        self.continue_button = QPushButton()

        size_policy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        # sizePolicy4.setHorizontalStretch(0)
        # sizePolicy4.setVerticalStretch(0)
        # sizePolicy4.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(size_policy)
        self.continue_button.setSizePolicy(size_policy)
        self.continue_button.setDisabled(True)

        self.checkbox = QCheckBox()
        self.checkbox.setText("Don't show this again")
        
        self.grid_layout.addItem(horizontal_spacer, 8, 2, 1, 1)
        self.grid_layout.addWidget(self.checkbox, 9, 4, 1, 1)

        self.grid_layout.addWidget(self.cancel_button, 9, 5, 1, 1)
        self.cancel_button.setText("Cancel")

        self.grid_layout.addWidget(self.continue_button, 9, 6, 1, 1)
        self.continue_button.setText("Continue")
