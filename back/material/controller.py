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

    def add_materials_from_file(self, file):
        try:
            repository.create_new_materials(self.db, file)
            return {"success": True, "message": "Materials uploaded successfully!"}
        except Exception as e:
            return {"success": False, "error": f"Error during file processing: {str(e)}"}


