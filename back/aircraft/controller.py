from typing import List
from back.aircraft import repository
from back.utils.utils import json_response
from back.aircraft.schema import AircraftSchema

class AircraftController:
    def __init__(self, db, window = None):
        self.db = db
        self.window = window
    
    @json_response(List[AircraftSchema])
    def get_all_aircrafts(self):
        aircrafts = repository.get_all_aircrafs(self.db)
        
        return aircrafts


    def add_aircrafts_from_file(self, data: dict):
        # if data["name"] == "error":
        #     raise Exception("error")
        repository.create_new_aircrafts(self.db, data["file"])


