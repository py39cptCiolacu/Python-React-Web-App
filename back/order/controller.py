from typing import List
from back.order import repository
from back.utils.utils import json_response
from back.order.schema import OrderSchema

class OrderController:
    def __init__(self, db, window = None):
        self.db = db
        self.window = window

    @json_response(List[OrderSchema])
    def get_all_orders(self):
        orders = repository.get_all_orders(self.db)

        return orders

    def add_orders_from_file(self, data: dict):
        # if data["name"] == "error":
        #     raise Exception("error")
        repository.create_new_orders(self.db, data["file"])