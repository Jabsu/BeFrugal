from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Signal, QObject, Qt

from ui.duplicates_window import UI_Duplicates


class Duplicates(QObject):

    continue_signal = Signal()

    def __init__(self, data):
        QObject.__init__(self)
        self.data = data
        self.duplicates_to_keep = {}

    def show(self):
        self.dpl_ui = UI_Duplicates()
        self.dpl_ui.show()
        self.make_connections()
        self.retranslate_ui()

    def make_connections(self):
        self.dpl_ui.duplicate_list.itemSelectionChanged.connect(
            self.selection_buttons)
        self.dpl_ui.select_all_button.clicked.connect(
            self.dpl_ui.duplicate_list.selectAll)
        self.dpl_ui.deselect_all_button.clicked.connect(
            self.dpl_ui.duplicate_list.clearSelection)
        self.dpl_ui.continue_button.clicked.connect(self.continue_pressed)

    def continue_pressed(self):

        self.create_dict_from_selected_items()
        self.dpl_ui.hide()
        self.continue_signal.emit()


    def create_dict_from_selected_items(self):
        for selected_item in self.dpl_ui.duplicate_list.selectedItems():
            dic = selected_item.data(Qt.UserRole)
            for year, v in dic.items():
                for month, v2 in v.items():
                    for id, values in v2.items():
                        if not year in self.duplicates_to_keep:
                            self.duplicates_to_keep[year] = {}
                        if not month in self.duplicates_to_keep[year]:
                            self.duplicates_to_keep[year][month] = {}
                        self.duplicates_to_keep[year][month][id] = values


        
    def selection_buttons(self):
        list = self.dpl_ui.duplicate_list
        self.dpl_ui.select_all_button.setDisabled(
            len(list.selectedItems()) == len(self.data))
        self.dpl_ui.deselect_all_button.setDisabled(not list.selectedItems())

    def retranslate_ui(self):
        self.dpl_ui.duplicates_found_label.setText(
            f'Found <span style="font-weight:bold">{len(self.data)}</span> possible duplicates to previously imported transactions.')

        # self.list = []
        for entry in self.data:
            for year, month in entry.items():
                for id, data in month.items():
                    for id, transaction in data.items():
                        sanitized = f"{transaction['og_date'].ljust(12)} {str(transaction['amount']).ljust(12)} {transaction['entity']}"
                        item = QListWidgetItem()
                        item.setText(sanitized)
                        item.setData(Qt.UserRole, entry)

                        self.dpl_ui.duplicate_list.addItem(item)
                        # self.list.append(sanitized)
