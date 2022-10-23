import sys
import traceback
from datetime import date

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QMainWindow, QHeaderView, QStyledItemDelegate,
                               QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem, QWidget, QStyleFactory)

from ui.main_window import UI_MainWindow

from components.transactions import Transactions
from components.formatting import Formatting
from components.duplicates import Duplicates
from components.entities_found import EntitiesFound
from components.manage_json import ManageJSON

# import qdarktheme

class MainWindow(QMainWindow):
    def __init__(self, screen, app):
        super(MainWindow, self).__init__()
        self.ui = UI_MainWindow()
        self.screen = screen
        self.app = app
        #  app.setStyleSheet(qdarktheme.load_stylesheet())

        self.first_resize = True

        self.load_settings()

        height = self.settings["main_window_height"]
        width = self.settings["main_window_width"]
        self.ui.setup_ui(self, height, width)

        self.tabs = {}
        self.tables = {}

        self.create_menu_connections()

        self.entities = {'Payer': {}, 'Recipient': {}}
        self.averages_per_year = {}

        self.transactions = Transactions()
        self.transactions.first_run()

        if self.transactions.items:
            self.entities = self.transactions.known_entities
            # self.create_categories()
            self.create_tables_from_data()
            self.load_comments()

    def closeEvent(self, event):
        self.settings["main_window_width"] = self.size().width()
        self.settings["main_window_height"] = self.size().height()
        self.save_settings()
        self.save_comments()
        try:
            event.accept()
        except AttributeError:
            self.app.quit()

    def load_settings(self):
        self.db = ManageJSON("settings.json")
        self.db.read_data()

        if not self.db.data:
            self.load_defaults()
        else:
            self.settings = self.db.data

    def load_comments(self):
        com_db = ManageJSON("comments.json")
        com_db.read_data()

        if d := com_db.data:
            for year, values in d.items():
                for row, text in values.items():
                    try:
                        table = self.tables[year]
                    except KeyError:
                        continue
                    table.setItem(int(row)-1, self.comment_column,
                                  QTableWidgetItem())
                    cell = table.item(int(row)-1, self.comment_column)
                    cell.setText(text)

    def save_comments(self):
        com_db = ManageJSON("comments.json")
        dic = {}

        for year, table in self.tables.items():
            for row in range(0, table.rowCount()):
                item = table.item(row, self.comment_column)
                try:
                    item.text()
                except AttributeError:
                    continue
                try:
                    dic[year][row+1] = item.text()
                except KeyError:
                    dic[year] = {row+1: item.text()}

        com_db.save_data(dic)

    def save_settings(self):
        self.db.save_data(self.settings)

    def load_defaults(self):
        '''Default settings'''

        self.settings = {
            "main_window_height": int(screen.height() / 2 + 55),
            "main_window_width": int(screen.width() / 2),
            "show_formatting_window": True,
            "theme": "Fusion",
            "save_target": "10000",
            "currency": "EUR",
        }

    def create_menu_connections(self):
        self.ui.menu_import_from_file.triggered.connect(self.read_file)
        self.ui.menu_import_from_clipboard.triggered.connect(
            self.read_clipboard)
        self.ui.menu_quit.triggered.connect(self.closeEvent)
        self.ui.menu_settings.triggered.connect(self.open_settings_dialog)

    def open_settings_dialog(self):
        pass

    def calculate_eta(self):
        tab = self.ui.tab_widget.currentWidget().objectName()
        avg = float(self.averages_per_year[tab])
        input_value = self.ui.money_input.text()
        try:
            months = round(float(input_value) / avg, 1)
        except:
            return
        else:
            if months == 0.0:
                eta = '<span style="font-weight:bold">no time</span>'
            else:
                eta = f'<span style="font-weight:bold">{months} months</span>'
            self.ui.eta_calculation.setText(f"it would take {eta} to save")
            self.settings["save_target"] = str(input_value)

    def read_file(self):
        file = QFileDialog.getOpenFileName(
            self, 'Choose a file with transactions')[0]
        if not file:
            return
        try:
            with open(file, 'r', encoding="utf-8") as f:
                self.data = f.readlines()
        except:
            self.ui.popup(traceback.format_exc(), QMessageBox.Critical)
        else:
            self.open_formatting_dialog()

    def read_clipboard(self):
        try:
            clipboard = QApplication.clipboard().text()
        except:
            self.ui.popup(traceback.format_exc(), QMessageBox.Critical)
        else:
            if clipboard:
                self.data = clipboard.split('\n')
                self.open_formatting_dialog()
            else:
                self.ui.popup("There is no text in your clipboard.",
                              QMessageBox.Information)

    def open_formatting_dialog(self):

        if not self.settings["show_formatting_window"]:
            return self.import_data()

        self.fmt_dialog = Formatting(self.data)
        self.fmt_dialog.get_sample()
        self.fmt_dialog.continue_signal.connect(
            self.fmt_dialog_continue_pressed)

        if not self.fmt_dialog.sample:
            self.ui.popup(
                "It seems the data you are trying to import is full of nothing.", QMessageBox.Warning)
            return
        else:
            self.fmt_dialog.show()

    def fmt_dialog_continue_pressed(self):
        self.settings["show_formatting_window"] = self.fmt_dialog.show_window
        self.save_settings()
        self.import_data()

    def import_data(self):

        self.transactions = Transactions(self.data)
        self.transactions.import_new_data(self.fmt_dialog.preset)

        if len(self.transactions.duplicates):
            self.dpl_dialog = Duplicates(self.transactions.duplicates)
            self.dpl_dialog.show()
            self.dpl_dialog.continue_signal.connect(
                self.keep_selected_duplicates)
        elif self.transactions.items:
            self.final_phase()

    def keep_selected_duplicates(self):

        if dups := self.dpl_dialog.duplicates_to_keep:
            self.transactions.merge_duplicates(dups)
        self.final_phase()

    def new_entities_found(self):
        self.new_entities_dialog = EntitiesFound(
            self.transactions.new_entities)
        self.new_entities_dialog.show()
        self.new_entities_dialog.continue_signal.connect(self.merge_entities)

    def merge_entities(self):

        ent_db = ManageJSON('entities.json')
        self.entities['Payer'] = self.transactions.known_entities['Payer'] | self.new_entities_dialog.selections['Payer']
        self.entities['Recipient'] = self.transactions.known_entities['Recipient'] | self.new_entities_dialog.selections['Recipient']
        ent_db.save_data(self.entities)
        self.create_tables_from_data()

    def create_categories(self):
        self.categories = []

        # Create a list of categories
        for counterparty in ("Payer", "Recipient"):
            for ent, values in self.entities[counterparty].items():
                if values['category'] not in self.categories:
                    self.categories.append(values['category'])

        if not self.categories:
            self.categories = [
                "Uncategorized Expenses", "Uncategorized Income"]

        self.categories = sorted(self.categories)

    def final_phase(self):

        self.transactions.save_imported_data()
        if (self.transactions.new_entities['Payer']
                or self.transactions.new_entities['Recipient']):
            self.new_entities_found()
        else:
            self.create_tables_from_data()

    def create_tables_from_data(self):

        self.create_categories()

        self.ui.temp_info.hide()

        for year in self.transactions.items.keys():
            self.year = str(year)
            self.create_table()
            self.add_items_to_table()
            self.totals_and_averages()

        self.ui.create_savings_target_grid()
        self.ui.money_input.setText(self.settings["save_target"])
        self.ui.money_input.textChanged.connect(self.calculate_eta)
        self.ui.currency_label.setText(self.settings['currency'])
        self.calculate_eta()

    def create_table(self):

        if self.year in self.tables.keys():
            tab = self.tabs[self.year]
            table = self.tables[self.year]
            table.deleteLater()
        else:
            # Create new tab
            tab = QWidget()
            self.ui.tab_widget.addTab(tab, self.year)
            tab.setObjectName(self.year)
            self.tabs[self.year] = tab

            grid = QGridLayout(tab)
            grid.setObjectName(self.year)

        # Create and configure new table
        table_widget = QTableWidget(tab)
        table_widget.setObjectName(self.year)

        grid = tab.findChild(QGridLayout, self.year)

        grid.addWidget(table_widget, 0, 0, 1, 1)

        self.ui.configure_table(table_widget)

        table_widget.setWordWrap(True)

        self.tables[self.year] = table_widget

        self.table = table_widget

        # Create columns (you wouldn't have guessed this)
        self.create_columns()

    def create_columns(self):
        '''Create columns for the table.'''
        table = self.table

        def add_column(name):
            n = table.columnCount()
            table.setColumnCount(n+1)
            table.setHorizontalHeaderItem(n, QTableWidgetItem())
            item = table.horizontalHeaderItem(n)
            item.setText(name)
            item.setTextAlignment(self.ui.cell_align)

            # font = QFont()
            # if name == 'Difference' or name == 'Net':
            #    font.setItalic(True)
            # else:
            #    font.setItalic(False)
            # item.setFont(font)
            return item

        # Create initial columns
        add_column('Total Income')
        add_column('Total Expenses')
        item = add_column('Net')
        item.setData(Qt.UserRole, 'Net')

        # Create columns from categories
        for category in self.categories:
            add_column(category)
            item = add_column('Diff.')
            item.setData(Qt.UserRole, 'Difference')

        item = add_column('Comments')
        item.setData(Qt.UserRole, 'Comments')
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # Apply header styles
        header = self.table.horizontalHeader()
        delegate = ReadOnlyDelegate(table)
        for col in range(0, table.columnCount()):
            h_item = table.horizontalHeaderItem(col)
            if (h_item.data(Qt.UserRole) == 'Difference' or
               h_item.data(Qt.UserRole) == 'Net'):
                header.setSectionResizeMode(col, QHeaderView.ResizeToContents)
                table.setItemDelegateForColumn(col, delegate)
            elif (h_item.data(Qt.UserRole) == 'Comments'):
                self.comment_column = col
                # header.setSectionResizeMode(col, QHeaderView.ResizeToContents)
                # header.setMaximumSectionSize(screen.width() / 4)
                header.setStretchLastSection(True)
            else:
                table.setItemDelegateForColumn(col, delegate)
                header.setSectionResizeMode(col, QHeaderView.ResizeToContents)
        


    def create_vertical_header(self, header: str) -> object:
        n = self.table.rowCount()
        self.table.setRowCount(n+1)
        self.table.setVerticalHeaderItem(n, QTableWidgetItem())
        item = self.table.verticalHeaderItem(n)
        item.setText(header)
        item.setTextAlignment(self.ui.header_align)
        return item

    def create_list_of_transaction_objects(self):

        self.transactions = Transactions(self.tr_data, self.bank)

    def add_items_to_table(self):
        items = self.transactions.items

        for month in range(1, 13):
            try:
                items[self.year][str(month)]
            except:
                continue

            month_name = date(1, month, 1).strftime('%B')
            item = self.create_vertical_header(month_name)
            item.setData(Qt.UserRole, 'month')
            sums = self.sums_per_entity(str(month))

            for column, sum in sums.items():
                # create cells with sums
                if sum != 0:
                    self.place_item_to_cell(month_name, column, sum)

            self.calculate_diffs()

    def place_item_to_cell(self, month, column, sum):
        table = self.table
        rows = table.rowCount()
        for row in range(0, rows):
            if table.verticalHeaderItem(row).text() == month:
                break
        cols = table.columnCount()
        for col in range(0, cols):
            if table.horizontalHeaderItem(col).text() == column:
                break

        table.setItem(row, col, QTableWidgetItem())
        item = table.item(row, col)
        item.setText(str(sum).replace('-', ''))
        item.setTextAlignment(self.ui.cell_align)

    def calculate_diffs(self):
        table = self.table

        def create_cell(table, row, col, text):
            table.setItem(row, col, QTableWidgetItem())
            item = table.item(row, col)
            item.setText(str(difference))
            item.setTextAlignment(self.ui.cell_align)
            return item

        for col in range(0, table.columnCount()):
            h_item = table.horizontalHeaderItem(col)

            if h_item.data(Qt.UserRole) == 'Difference':
                for row in range(0, table.rowCount()):
                    previous_value = None
                    current_value = None
                    if item := table.item(row, col-1):
                        current_value = float(item.text())
                    for r in range(1, 11):
                        if item := table.item(row - r, col-1):
                            previous_value = float(item.text())
                            break
                    if current_value and previous_value:
                        difference = round(
                            current_value - previous_value, 2)
                        item = create_cell(table, row, col, difference)
                        if difference > 0:
                            item.setForeground(self.ui.red)
                        else:
                            item.setForeground(self.ui.green)

            elif h_item.data(Qt.UserRole) == 'Net':
                for row in range(0, table.rowCount()):
                    income = 0
                    expenses = 0
                    if item := table.item(row, col-2):
                        income = float(item.text())
                    if item := table.item(row, col-1):
                        expenses = float(item.text())
                    difference = round(income - expenses, 2)
                    item = create_cell(table, row, col, difference)
                    if difference < 0:
                        item.setForeground(self.ui.red)
                    else:
                        item.setForeground(self.ui.green)

    def sums_per_entity(self, month):
        items = self.transactions.items
        ret = {'Total Income': 0, 'Total Expenses': 0}

        for column in self.categories:
            ret[column] = 0

        for transaction in items[self.year][month].values():
            try:
                amount = transaction['amount']
                entity = transaction['entity'].title()
            except KeyError:
                continue
            if amount > 0:
                ret['Total Income'] = round(ret['Total Income'] + amount, 2)
                counterparty = 'Payer'
                default_category = 'Uncategorized Income'
            else:
                ret['Total Expenses'] = round(
                    ret['Total Expenses'] + amount, 2)
                counterparty = 'Recipient'
                default_category = 'Uncategorized Expenses'

            try:

                column = self.entities[counterparty][entity]['category']
            except Exception as e:
                column = default_category
                # print(f"No category set for {entity} ({counterparty})")

            ret[column] = round(ret[column] + amount, 2)

            # if not matches and amount < 0:
            # ret['Uncategorized'] = round(ret['Uncategorized'] + amount, 2)

        return ret

    def totals_and_averages(self):
        table = self.table
        rows = 0

        font = QFont()
        font.setBold(True)

        for header in ['', 'Average', 'Total']:
            item = self.create_vertical_header(header)
            item.setFont(font)

        for col in range(0, table.columnCount()):
            h_item = table.horizontalHeaderItem(col)
            total = 0
            items = 0
            for row in range(0, table.rowCount()):
                v_item = table.verticalHeaderItem(row)
                if v_item.data(Qt.UserRole) == 'month':
                    rows += 1
                    if table.item(row, col):
                        total += float(table.item(row, col).text())
                        items += 1
            if items:
                avg = str(round(total / items, 2))
                total = str(round(total, 2))
                if h_item.data(Qt.UserRole) == 'Net':
                    self.averages_per_year[self.year] = avg
                r = row-1
                for val in [avg, total]:
                    table.setItem(r, col, QTableWidgetItem())
                    item = table.item(r, col)
                    item.setText(val)
                    item.setTextAlignment(self.ui.cell_align)
                    r += 1


class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen().size()
    window = MainWindow(screen, app)
    window.show()
    sys.exit(app.exec())
