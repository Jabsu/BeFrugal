
from PySide6.QtCore import QCoreApplication, Qt, QSize
from PySide6.QtGui import QAction, QBrush, QColor, QIntValidator
from PySide6.QtWidgets import (QAbstractItemView, QComboBox, QGridLayout, QLabel, QLayout, QLineEdit,
                               QMenu, QMenuBar, QSizePolicy, QSpacerItem, QTabWidget, QWidget, QMessageBox)


class UI_MainWindow(object):
    def setup_ui(self, MainWindow, height, width):
        
        MainWindow.resize(width, height)
        MainWindow.setWindowTitle("BeFrugal")

        self.menubar = QMenuBar(MainWindow)
        self.menu_file = QMenu(self.menubar)
        self.menu_import_transactions = QMenu(self.menu_file)
        self.menu_import_transactions.setTitle('Import transactions')
        MainWindow.setMenuBar(self.menubar)

        # create menu objects
        menu_items = {
            'menu_quit': 'Quit',
            'menu_import_from_file': 'From a file...',
            'menu_import_from_clipboard': 'From the clipboard',
            'menu_settings': 'Settings'
        }

        for var_name, text in menu_items.items():
            setattr(self, var_name, QAction(MainWindow))
            getattr(self, var_name).setText(text)

        self.menu_import_transactions.addAction(self.menu_import_from_file)
        self.menu_import_transactions.addAction(
            self.menu_import_from_clipboard)

        self.menu_file.setTitle("Menu")
        self.menubar.addAction(self.menu_file.menuAction())
        self.menu_file.addAction(self.menu_import_transactions.menuAction())
        self.menu_file.addAction(self.menu_settings)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.menu_quit)

        # self.actionImport_transactions = QAction(MainWindow)
        # self.actionImport_transactions.setObjectName(u"actionImport_transactions")
        # self.actionQuit = QAction(MainWindow)
        # self.actionQuit.setObjectName(u"actionQuit")

        self.central_widget = QWidget(MainWindow)

        self.grid_layout = QGridLayout(self.central_widget)
        self.tab_widget = QTabWidget(self.central_widget)
        self.grid_layout.addWidget(self.tab_widget, 0, 0, 1, 1)

        self.temp_info = QLabel(self.central_widget)
        self.temp_info.setAlignment(Qt.AlignCenter)

        self.grid_layout.addWidget(self.temp_info, 0, 0, 1, 1)

        self.temp_info.setText(
            '💡 Tip of the day: <span style="font-weight:bold">Menu</span> ⟶ <span style="font-weight:bold">Import transactions</span>')

        MainWindow.setCentralWidget(self.central_widget)

        # self.retranslateUi(MainWindow)
        # QMetaObject.connectSlotsByName(MainWindow)

        self.green = QBrush(QColor(0, 180, 87, 255))
        self.green.setStyle(Qt.SolidPattern)
        self.red = QBrush(QColor(255, 0, 0, 255))
        self.red.setStyle(Qt.SolidPattern)

        self.cell_align = Qt.AlignRight | Qt.AlignVCenter
        self.header_align = Qt.AlignRight | Qt.AlignVCenter

        # self.horizontal_spacer_top = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.grid_layout.addItem(self.horizontal_spacer_top, 0, 0, 1, 1)

        # self.create_savings_target_grid()

        # create horizontal spacers
        for row in [1, 3]:
            h_spacer = QSpacerItem(
                40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.grid_layout.addItem(h_spacer, row, 0, 1, 1)

    def configure_table(self, table):
        table.setAlternatingRowColors(True)
        table.setAcceptDrops(False)
        table.setDragEnabled(True)
        table.setSortingEnabled(False)
        table.setSelectionMode(QAbstractItemView.NoSelection)
        # table.setSelectionBehavior(QAbstractItemView.SelectItems)

    def create_savings_target_grid(self):
        self.savings_target_grid = QGridLayout()
        self.savings_target_grid.setObjectName(u"savings_target_grid")
        self.savings_target_grid.setSizeConstraint(QLayout.SetMaximumSize)
        self.savings_target_grid.setContentsMargins(-1, -1, 300, -1)
        self.according_to = QLabel(self.central_widget)
        self.according_to.setObjectName(u"according_to")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.according_to.sizePolicy().hasHeightForWidth())
        self.according_to.setSizePolicy(sizePolicy)

        self.savings_target_grid.addWidget(self.according_to, 2, 0, 1, 1)

        self.eta_calculation = QLabel(self.central_widget)
        self.eta_calculation.setObjectName(u"eta_calculation")
        sizePolicy.setHeightForWidth(
            self.eta_calculation.sizePolicy().hasHeightForWidth())
        self.eta_calculation.setSizePolicy(sizePolicy)
        self.eta_calculation.setMinimumSize(QSize(180, 16777215))
        self.eta_calculation.setMaximumSize(QSize(200, 16777215))

        self.savings_target_grid.addWidget(self.eta_calculation, 2, 2, 1, 1)

        self.money_input = QLineEdit(self.central_widget)
        self.money_input.setObjectName(u"money_input")
        sizePolicy.setHeightForWidth(
            self.money_input.sizePolicy().hasHeightForWidth())
        self.money_input.setSizePolicy(sizePolicy)
        self.money_input.setMinimumSize(QSize(50, 0))
        self.money_input.setMaximumSize(QSize(80, 16777215))

        self.currency_label = QLabel()

        validator = QIntValidator(10, 1000000000)
        self.money_input.setValidator(validator)

        self.savings_target_grid.addWidget(self.money_input, 2, 3, 1, 1)
        self.savings_target_grid.addWidget(self.currency_label, 2, 4, 1, 1)

        self.combo_box = QComboBox(self.central_widget)
        self.combo_box.addItem("")
        self.combo_box.addItem("")
        self.combo_box.addItem("")
        self.combo_box.addItem("")
        self.combo_box.setObjectName(u"combo_box")
        sizePolicy.setHeightForWidth(
            self.combo_box.sizePolicy().hasHeightForWidth())
        self.combo_box.setSizePolicy(sizePolicy)

        self.savings_target_grid.addWidget(self.combo_box, 2, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.savings_target_grid.addItem(self.horizontalSpacer, 2, 5, 1, 1)

        self.grid_layout.addLayout(self.savings_target_grid, 2, 0, 1, 1)

        # widget contents
        self.according_to.setText(QCoreApplication.translate(
            "MainWindow", u"According to ", None))
        # self.eta_calculation.setText(QCoreApplication.translate("MainWindow", u"it would take 2 years to save", None))
        self.combo_box.setItemText(0, QCoreApplication.translate(
            "MainWindow", u"selected year", None))
        self.combo_box.setItemText(1, QCoreApplication.translate(
            "MainWindow", u"last month", None))
        self.combo_box.setItemText(2, QCoreApplication.translate(
            "MainWindow", u"last 3 months", None))
        self.combo_box.setItemText(3, QCoreApplication.translate(
            "MainWindow", u"last 6 months", None))

    def popup(self, msg, icon=QMessageBox.Warning):
        box = QMessageBox()
        box.setText(msg)
        box.setIcon(icon)
        box.exec()

    def retranslate_ui(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"MainWindow", None))
