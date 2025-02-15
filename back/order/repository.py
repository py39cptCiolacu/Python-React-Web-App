from typing import List
import pandas as pd
from sqlalchemy.orm import Session
from back.models import Order

def get_all_orders(db: Session) -> List[Order]:
    orders = db.query(Order).all()
    return orders

def create_new_orders(db: Session, file_path: str):
    print(file_path)
    orders = pd.read_excel(file_path)

    for index, row in orders.iterrows():
        new_order = Order(
            aircraft_serial_number = row["Aircraft Serial Number"],
            material_part_number = row["Material PN"],
            arrival_date = row["Arrival Date"],
            status = row["Status"],
        )
        db.add(new_order)

    db.commit()
    db.close()

