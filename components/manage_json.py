
import json
import os

class ManageJSON:
    def __init__(self, file) -> None:
        self.data = None
        self.file = file
        
    def read_data(self) -> bool:
        if os.path.exists(self.file):
            with open(self.file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            
    def save_data(self, data=dict) -> None:
        with open(self.file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
    