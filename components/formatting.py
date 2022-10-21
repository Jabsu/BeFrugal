import re
from datetime import datetime

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal, QObject

from ui.formatting_window import UI_Formatting
from .manage_json import ManageJSON


class Formatting(QObject):

    continue_signal = Signal()

    def __init__(self, data) -> None:
        QObject.__init__(self)
        self.data = data
        self.sample = None
        self.formatted_sample = None
        # Defaults (if not saved)
        self.separator = ''
        self.date_index = -1
        self.amount_index = -1
        self.entity_index = -1
        self.date_format = ''
        # -----------------------
        self.finished = False
        self.valid = "\u2705"
        self.invalid = "\u274C"
        self.warning = "\u26A0"
        self.question = "\u2753"
        self.show_window = True

        self.db = ManageJSON('fmt_settings.json')

    def get_saved_settings(self) -> bool:
        self.db.read_data()
        preset_indexes = {'Preset 1': 0, 'Preset 2': 1, 'Preset 3': 2}
        if cfg := self.db.data:
            for preset, values in cfg.items():
                if not values:
                    continue
                self.separator = values['separator']
                self.date_index = values['date_index']
                self.amount_index = values['amount_index']
                self.entity_index = values['entity_index']
                self.date_format = values['date_format']
                if self.valid_spinboxes() and self.valid_date_format():
                    self.fmt_ui.cfg_preset.setCurrentIndex(preset_indexes[preset])
                    break

            return True
        return None

    def save_settings(self):
        self.read_ui_values()
        data = {}
        self.preset = self.fmt_ui.cfg_preset.currentText()
        data[self.preset] = {'separator': self.separator,
                'date_index': self.date_index,
                'amount_index': self.amount_index,
                'entity_index': self.entity_index,
                'date_format': self.date_format}
        if old_data := self.db.data:
            data = old_data | data
        
        self.db.save_data(data)

    def read_ui_values(self):
        self.separator = self.fmt_ui.separator.text()
        self.date_index = self.fmt_ui.date_spinbox.value()
        self.amount_index = self.fmt_ui.amount_spinbox.value()
        self.entity_index = self.fmt_ui.entity_spinbox.value()
        self.date_format = self.fmt_ui.date_format.text()

    def get_sample(self):

        for n in range(1, len(self.data)):
            try:
                self.data[-n]
            except IndexError:
                pass
            else:
                if len(self.data[-n]) > 20:
                    self.sample = self.data[-n]
                    break

    def show(self):
        self.fmt_ui = UI_Formatting()

        if not self.get_saved_settings():
            self.guess_separator()
            self.guess_indexes()

        self.format_sample()

        self.retranslate_ui()
        self.make_connections()
        if self.valid_spinboxes() and self.valid_date_format():
            self.fmt_ui.continue_button.setEnabled(True)

        self.fmt_ui.show()

    def make_connections(self):
        self.fmt_ui.date_spinbox.valueChanged.connect(
            self.ui_value_changed)
        self.fmt_ui.amount_spinbox.valueChanged.connect(
            self.ui_value_changed)
        self.fmt_ui.entity_spinbox.valueChanged.connect(
            self.ui_value_changed)
        self.fmt_ui.separator.textChanged.connect(
            self.ui_value_changed)
        self.fmt_ui.date_format.textChanged.connect(
            self.ui_value_changed)

        self.fmt_ui.continue_button.clicked.connect(self.continue_pressed)
        self.fmt_ui.cancel_button.clicked.connect(self.cancel_pressed)

    def continue_pressed(self):
        self.save_settings()
        self.fmt_ui.hide()
        self.finished = True
        self.show_window = not self.fmt_ui.checkbox.isChecked()
        self.continue_signal.emit()

    def cancel_pressed(self):
        self.fmt_ui.hide()

    def ui_value_changed(self):
        self.read_ui_values()
        self.format_sample()
        self.retranslate_ui()
        valid_spinboxes = self.valid_spinboxes()
        valid_date = self.valid_date_format()
        if valid_date and valid_spinboxes:
            self.fmt_ui.continue_button.setDisabled(False)
        else:
            self.fmt_ui.continue_button.setDisabled(True)

    def valid_date_format(self) -> bool:
        try:
            date_str = self.sample.split(self.separator.replace('%t', '\t'))[
                self.date_index]
        except (IndexError, ValueError):
            self.fmt_ui.separator_validity.setText(self.invalid)
            self.fmt_ui.date_format_validity.setText(self.invalid)
            self.fmt_ui.date_idx_validity.setText(self.invalid)
            return False
        else:
            self.fmt_ui.separator_validity.setText(self.valid)

        try:
            datetime.strptime(date_str, self.date_format)
        except ValueError:
            self.fmt_ui.date_format_validity.setText(self.invalid)
            self.fmt_ui.date_idx_validity.setText(self.question)
            # self.fmt_ui.date_format_validity.setToolTip("Invalid formatting")
            return False
        except re.error:
            self.fmt_ui.date_format_validity.setText(self.invalid)
            self.fmt_ui.date_idx_validity.setText(self.question)
            # self.fmt_ui.date_format_validity.setToolTip("Invalid formatting")
            return False
        else:
            self.fmt_ui.date_format_validity.setText(self.valid)
            # self.fmt_ui.date_format_validity.setToolTip("Valid formatting")
            return True

    def valid_spinboxes(self) -> bool:
        values = {1: [self.date_index, self.fmt_ui.date_idx_validity],
                  2: [self.amount_index, self.fmt_ui.amount_idx_validity],
                  3: [self.entity_index, self.fmt_ui.entity_idx_validity]}

        all_valid = True
        indexes = []

        try:
            sample_size = len(self.sample.split(self.separator.replace('%t', '\t')))
        except (IndexError, ValueError):
            sample_size = 1

        for key, items in values.items():
            idx, label = items

            if idx == -1:
                label.setText(self.invalid)
                all_valid = False
            elif idx in indexes:
                for idx2, label2 in values.values():
                    if idx == idx2:
                        label2.setText(self.warning)
                all_valid = False
            elif idx > sample_size:
                label.setText(self.invalid)
                all_valid = False
            else:
                label.setText(self.valid)
            indexes.append(idx)
        return all_valid

        '''
        if self.date_index == -1:
            self.fmt_ui.date_idx_validity.setText(self.invalid)

        if -1 in values:
            return False
        elif len(set(values)) < len(values):
            return False

        return True
        '''

    def guess_separator(self):
        common_separators = [',', ';', '\t']
        for sep in common_separators:
            if len(re.findall(sep, self.sample)) >= 2:
                self.separator = sep
                
    def guess_indexes(self):
        idx = 0
        common_date_formats = [
            '%d.%m.%Y', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d',
            '%Y%d%m', '%d%m%Y', '%m%d%Y'
        ]

        for item in self.sample.split(self.separator):

            for fmt in common_date_formats:
                try:
                    datetime.strptime(item, fmt)
                except ValueError:
                    pass
                else:
                    self.date_index = idx
                    self.date_format = fmt

            # if self.date_index == -1:
            #    if (len(re.findall('/', item)) > 1 or
            #            len(re.findall('\.', item)) > 1 or
            #            len(item) == 8):
            #        self.date_index = idx

            if len(re.findall('\.|,', item)) == 1:
                self.amount_index = idx

            if len(re.findall('[a-z]', item, re.I)) >= 4 and self.entity_index == -1:
                self.entity_index = idx

            idx += 1

    def format_sample(self):

        if not self.separator:
            return

        idx = 0
        temp_list = []

        for item in self.sample.split(self.separator.replace('%t', '\t')):
            formatted_item = item
            if self.date_index == idx:
                formatted_item = f"{self.fmt_ui.d_span}{item}</span>"
            if self.amount_index == idx:
                formatted_item = f"{self.fmt_ui.a_span}{item}</span>"
            if self.entity_index == idx:
                formatted_item = f"{self.fmt_ui.e_span}{item}</span>"
            temp_list.append(formatted_item)
            idx += 1

        self.formatted_sample = self.separator.replace(
            '%t', '\t').join(temp_list)

    def retranslate_ui(self):

        # Sample box
        if self.formatted_sample:
            self.fmt_ui.sample.setText(self.formatted_sample)
        else:
            self.fmt_ui.sample.setText(self.sample)

        sep = self.separator
        if self.separator == '\t':
            sep = '%t'
        self.fmt_ui.separator.setText(sep)

        # Spinbox values
        if self.date_index != -1:
            self.fmt_ui.date_spinbox.setValue(self.date_index)
        if self.amount_index != -1:
            self.fmt_ui.amount_spinbox.setValue(self.amount_index)
        if self.entity_index != -1:
            self.fmt_ui.entity_spinbox.setValue(self.entity_index)

        # Date format value
        self.fmt_ui.date_format.setText(self.date_format)
