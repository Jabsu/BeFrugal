from PySide6.QtWidgets import QStyleFactory
from PySide6.QtCore import Signal, QObject

from ui.settings_window import UI_Settings
from components.manage_json import ManageJSON
from components.config_categories import ConfigCategories
# 
import qdarktheme

class Settings(QObject):

    close_signal = Signal()

    def __init__(self, settings, app, entities):
        QObject.__init__(self)
        self.settings = settings
        self.entities = entities
        self.app = app

    def show(self):
        self.cfg_ui = UI_Settings()
        self.cfg_ui.show()
        self.make_connections()
        self.retranslate_ui()

    def retranslate_ui(self):
        for style in QStyleFactory.keys():
            self.cfg_ui.themes.addItem(style)

        self.cfg_ui.themes.addItem("qdarktheme")

        idx = self.cfg_ui.themes.findText(self.settings['theme'])
        if idx != -1: 
            self.cfg_ui.themes.setCurrentIndex(idx)
        
        self.cfg_ui.currency.setText(self.settings['currency'])
        self.cfg_ui.show_fmt_dialog_toggle.setChecked(self.settings["show_formatting_window"])

        db = ManageJSON('entities.json')
        db.read_data()
        db2 = ManageJSON('transactions.json')
        db2.read_data()
        if not db.data or not db2.data:
            self.cfg_ui.configure_categories.setEnabled(False)

    
        
    def make_connections(self):
        self.cfg_ui.themes.currentIndexChanged.connect(self.change_theme)
        self.cfg_ui.close_signal.connect(self.close)
        self.cfg_ui.configure_categories.clicked.connect(self.config_categories)

    def config_categories(self):
        self.config_cats = ConfigCategories(self.entities)
        self.config_cats.show()
        
    def change_theme(self):
        theme = self.cfg_ui.themes.currentText()
        if theme == "qdarktheme":
            self.app.setStyleSheet(qdarktheme.load_stylesheet())
        else:
            self.app.setStyleSheet("")
            self.app.setStyle(theme)
        
    def close(self):
        self.settings['currency'] = self.cfg_ui.currency.text()
        self.settings['theme'] = self.cfg_ui.themes.currentText()
        self.settings['show_formatting_window'] = self.cfg_ui.show_fmt_dialog_toggle.isChecked()
        self.close_signal.emit()
        


