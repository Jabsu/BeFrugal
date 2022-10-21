from PySide6.QtWidgets import QLabel, QComboBox
from PySide6.QtCore import Signal, QObject

from ui.new_entities_window import UI_NewEntities

class EntitiesFound(QObject):

    continue_signal = Signal()

    def __init__(self, entities):
        QObject.__init__(self)
        self.entities = entities
        self.selections = {'Payer': {}, 'Recipient': {}}
        self.new_categories = []

    def show(self):
        self.ent_ui = UI_NewEntities()
        self.ent_ui.show()
        self.make_connections()
        self.add_items()

    def make_connections(self):
        self.ent_ui.continue_button.clicked.connect(self.continue_pressed)
        self.ent_ui.add_category_button.clicked.connect(self.add_category)

    def add_category(self):
        txt = self.ent_ui.new_category.text()
        if not txt in self.new_categories:
            for combobox in self.ent_ui.findChildren(QComboBox):
                combobox.addItem(txt)
            self.ent_ui.new_category.setText('')
            self.ent_ui.category_added.setText(f'<span style="font-style:italic">{txt}</span> created and is now selectable.')
            self.new_categories.append(txt)
        else:
            self.ent_ui.new_category.setText('')
            self.ent_ui.category_added.setText(f'<span style="font-style:italic">{txt}</span> already exists.')

            
    def add_items(self):
        row = 1
        for counterparty, entities in self.entities.items():
            for entity, occurrence in entities.items():
                entity_label = QLabel(self.ent_ui.scroll_area_contents)
                entity_label.setText(entity)
                occurrence_label = QLabel(self.ent_ui.scroll_area_contents)
                occurrence_label.setText(str(occurrence))
                type_label = QLabel(self.ent_ui.scroll_area_contents)
                if counterparty == 'Payer':
                    color = 'green'
                    default_category = "Uncategorized Income"
                else:
                    color = 'red'
                    default_category = "Uncategorized Expenses"
                type_label.setText(f'<span style="color:{color}">{counterparty}')

                category_selector = QComboBox(self.ent_ui.scroll_area_contents)
                category_selector.addItem(default_category)
                category_selector.setObjectName(f"{entity}---{counterparty}")
                # category_selector.setEditable(True)
            
                self.ent_ui.grid_layout_2.addWidget(entity_label, row, 0, 1, 1)
                self.ent_ui.grid_layout_2.addWidget(occurrence_label, row, 1, 1, 1)
                self.ent_ui.grid_layout_2.addWidget(type_label, row, 2, 1, 1)
                self.ent_ui.grid_layout_2.addWidget(category_selector, row, 3, 1, 1)
                row += 1

    def get_selections(self):
        for selection in self.ent_ui.findChildren(QComboBox):
            entity, counterparty = selection.objectName().split("---")
            category = selection.currentText()
            self.selections[counterparty][entity] = {'category': category}

        sorted_payers = dict(sorted(self.selections['Payer'].items()))
        sorted_recipients = dict(sorted(self.selections['Recipient'].items()))
        
        self.selections['Payer'] = sorted_payers
        self.selections['Recipient'] = sorted_recipients

    def continue_pressed(self):
        self.ent_ui.hide()
        self.get_selections()
        self.continue_signal.emit()

    


