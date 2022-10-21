
import traceback
from datetime import datetime
from time import time as epoch

import config
from .manage_json import ManageJSON


class Transactions:

    def __init__(self, transaction_data=None):
        self.transaction_data = transaction_data
        
        self.db = ManageJSON(config.DATABASE)
        self.ent_db = ManageJSON('entities.json')
        self.load_known_entities()
        
        self.objects = []  # list of transaction objects
        self.items = {}  # dictionary of transactions
        self.old_data = {}  # previous imports
        self.duplicates = []  # list of duplicate transactions
        self.new_entities = {'Payer': {}, 'Recipient': {}}

    def load_known_entities(self):
        self.ent_db.read_data()
        if self.ent_db.data:
            self.known_entities = self.ent_db.data
        else:
            self.known_entities = {'Payer': {}, 'Recipient': {}}

    #def save_entity_configurations(self, configurations):
    #    self.ent_db.save_data(configurations)

    def first_run(self):
        self.get_previous_imports()
        if self.old_data:
            self.items = self.old_data
            # self.create_dict_of_transactions()

    def import_new_data(self, preset):
        self.preset = preset
        self.create_list_of_transaction_objects()
        self.get_previous_imports()
        self.create_dict_of_transactions()

    def create_list_of_transaction_objects(self):
        for transaction in self.transaction_data:
            t = Transaction(transaction, self.preset)
            if t.date and t.amount and t.entity:
                self.objects.append(t)

    def get_previous_imports(self):
        try:
            self.db.read_data()
        except:
            print(traceback.format_exc())
        else:
            if self.db.data:
                self.old_data = self.db.data
                self.items = self.old_data

    def create_dict_of_transactions(self):

        id = 0

        for transaction in self.objects:

            year = str(transaction.date.year)
            month = str(transaction.date.month)
            day = str(transaction.date.day)

            key_string = ''
            for key in [year, month, id]:
                key_string += f"['{key}']"
                try:
                    exec(f"self.items{key_string}")
                except KeyError:
                    exec(f"self.items{key_string} = {{}}")

            duplicate = False

            # Check for (and save) duplicates by comparing new data with previously imported data
            try:
                self.old_data[year][month]
            except KeyError:
                pass
            else:
                for entry in self.old_data[year][month].values():
                    if entry:
                        if (entry['amount'] == transaction.amount and
                                entry['entity'] == transaction.entity and
                                entry['day'] == day):
                            self.duplicates.append({year: {month: {str(id): {
                                'amount': entry['amount'],
                                'entity': entry['entity'],
                                'day': entry['day'],
                                'og_date': entry['og_date'],
                            }}}})
                            duplicate = True

            if not duplicate:
                self.items[year][month][str(id)] = {
                    'amount': transaction.amount,
                    'entity': transaction.entity,
                    'day': day,
                    'og_date': transaction.og_date
                }

            if transaction.amount > 0:
                counterparty = 'Payer'
                default_category = 'Uncategorized Income'
            else:
                counterparty = 'Recipient'
                default_category = 'Uncategorized Expenses'
            
            entity = transaction.entity.title()

            if not entity in self.known_entities[counterparty]:
                self.known_entities[counterparty][entity] = {'category': default_category}
            
            self.new_entities[counterparty][entity] = self.new_entities[counterparty].get(entity, 0) + 1

            id += 1

        sorted_payers = dict(sorted(self.new_entities['Payer'].items(),
                    reverse=True, key=lambda item: item[1]))
        sorted_recipients = dict(sorted(self.new_entities['Recipient'].items(),
                    reverse=True, key=lambda item: item[1]))

        self.new_entities['Payer'] = sorted_payers
        self.new_entities['Recipient'] = sorted_recipients

        sorted_payers = dict(sorted(self.known_entities['Payer'].items()))
        sorted_recipients = dict(sorted(self.known_entities['Recipient'].items()))
        
        self.known_entities['Payer'] = sorted_payers
        self.known_entities['Recipient'] = sorted_recipients


        

    def save_imported_data(self):
        self.db.save_data(self.items)

    def merge_duplicates(self, duplicates):

        d = duplicates

        n = 0
        for year, v in d.items():
            for month, v2 in v.items():
                for id, values in v2.items():
                    n += 1
                    id = f"dupl_{n}_{epoch()}"
                    self.items[year][month][id] = values


class Transaction:

    def __init__(self, transaction, preset):
        f = ManageJSON('fmt_settings.json')
        f.read_data()
        self.cfg = f.data[preset]

        self.trans = transaction
        self.set_date()
        self.set_amount()
        self.set_entity()

    def set_date(self):
        index = self.cfg['date_index']
        try:
            self.date = self.create_date_object(self.get_item(index))
            self.og_date = self.get_item(index)
        except:
            self.date = None

    def set_amount(self):
        index = self.cfg['amount_index']
        self.amount = self.get_item(index)
        try:
            self.amount = float(self.amount.replace(',', '.'))
        except:
            self.amount = None

    def set_entity(self):
        index = self.cfg['entity_index']
        self.entity = self.get_item(index)

    def get_item(self, index):
        try:
            ret = self.trans.split(
                self.cfg['separator'].replace('%t', '\t'))[index]
        except IndexError:
            ret = None
        return ret

    def is_income(self):
        return self.amount > 0

    def create_date_object(self, date):
        return datetime.strptime(date, self.cfg['date_format'])
