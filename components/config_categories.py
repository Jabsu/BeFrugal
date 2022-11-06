from PySide6.QtWidgets import QLabel, QComboBox
from PySide6.QtCore import QObject

from ui.configure_categories_window import UI_ConfigCategories
from components.manage_json import ManageJSON

class ConfigCategories(QObject):
    def __init__(self, entities):
        QObject.__init__(self)
        self.entities = entities
        self.new_categories = []
    
    def show(self):
        self.ui = UI_ConfigCategories()
        self.ui.show()
        self.add_entities()
        self.make_connections()
        
    def load_entities_with_categories(self):
        self.db = ManageJSON("entities.json")
        self.db.read_data()
        self.ents_with_cats = self.db.data

    def make_connections(self):
        self.ui.add_category_button.clicked.connect(self.add_category)
        self.ui.close_signal.connect(self.save_selections)

    def save_selections(self):
        
        for selection in self.ui.findChildren(QComboBox):
            entity, counterparty = selection.objectName().split("---")
            category = selection.currentText()
            self.entities[counterparty][entity] = {'category': category}
        
        sorted_payers = dict(sorted(self.entities['Payer'].items()))
        sorted_recipients = dict(sorted(self.entities['Recipient'].items()))
        
        self.entities['Payer'] = sorted_payers
        self.entities['Recipient'] = sorted_recipients

        self.db.save_data(self.entities)


    def add_entities(self):
        row_L = 0
        row_R = 0
        self.load_entities_with_categories()

        for counterparty, entities in self.entities.items():
            for entity, occurrence in entities.items():
                print(entity, occurrence)
                entity_label = QLabel(self.ui.scroll_area_L_contents)
                entity_label.setText(entity)
                occurrence_label = QLabel(str(occurrence))

                category_selector = QComboBox()
                category_selector.addItem(self.ents_with_cats[counterparty][entity]['category'])
                category_selector.setObjectName(f"{entity}---{counterparty}")

                if counterparty == 'Payer':
                    row_L += 1
                    self.ui.grid_L.addWidget(entity_label, row_L, 0, 1, 1)
                    self.ui.grid_L.addWidget(occurrence_label, row_L, 1, 1, 1)
                    self.ui.grid_L.addWidget(category_selector, row_L, 2, 1, 1)

                else:
                    row_R += 1
                    self.ui.grid_R.addWidget(entity_label, row_R, 0, 1, 1)
                    self.ui.grid_R.addWidget(occurrence_label, row_R, 1, 1, 1)
                    self.ui.grid_R.addWidget(category_selector, row_R, 2, 1, 1)


                

    def add_category(self):
        txt = self.ui.new_category.text()
        if not txt in self.new_categories:
            for combobox in self.ui.findChildren(QComboBox):
                combobox.addItem(txt)
            self.ui.new_category.setText('')
            self.ui.category_added.setText(f'<span style="font-style:italic">{txt}</span> created and is now selectable.')
            self.new_categories.append(txt)
        else:
            self.ui.new_category.setText('')
            self.ui.category_added.setText(f'<span style="font-style:italic">{txt}</span> already exists.')

