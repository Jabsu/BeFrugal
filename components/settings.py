from PySide6.QtWidgets import QStyleFactory
from PySide6.QtCore import Signal, QObject

from ui.settings_window import UI_Settings
from components.manage_json import ManageJSON
import qdarktheme

class Settings(QObject):

    close_signal = Signal()

    def __init__(self, settings, app):
        QObject.__init__(self)
        self.settings = settings
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
        
    def make_connections(self):
        self.cfg_ui.themes.currentIndexChanged.connect(self.change_theme)
        self.cfg_ui.close_signal.connect(self.close)
        
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
        


