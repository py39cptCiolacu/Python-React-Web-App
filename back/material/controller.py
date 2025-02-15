from typing import List
from back.material import repository
from back.utils.utils import json_response
from back.material.schema import MaterialSchema

class MaterialController:
    def __init__(self, db, window = None):
        self.db = db
        self.window = window
    
    @json_response(List[MaterialSchema])
    def get_all_materials(self):
        materials = repository.get_all_materials(self.db)
        
        return materials


    def add_materials_from_file(self, data: dict):
        # if data["name"] == "error":
        #     raise Exception("error")
        repository.create_new_materials(self.db, data["file"])


