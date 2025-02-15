from typing import List
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from back.models import Order, Aircraft, Material

def get_all_orders(db: Session) -> List[Order]:
    orders = db.query(Order).all()
    return orders

def create_new_orders(db: Session, file_path: str):
    print(file_path)
    orders = pd.read_excel(file_path)
    valid_orders = []

    for index, row in orders.iterrows():
        new_order = Order(
            aircraft_serial_number = row["Aircraft Serial Number"],
            material_part_number = row["Material PN"],
            arrival_date = row["Arrival Date"],
            status = row["Status"],
        )

        if _verify_order_before_add(db, new_order):
            valid_orders.append(new_order)
        else:
            ### user error with all that failed
            print(f"Order for aircraft {new_order.aircraft_serial_number} with material {new_order.material_part_number} skipped due to validation error!")

    if valid_orders:
        try:
            db.add_all(valid_orders)
            db.commit()
            #user info
        except IntegrityError:
            db.rollback()
            #error during database commit
        except Exception as e:
            db.rollback()
            #unexpected error
    else:
        #inform user- no valid data
        pass

def _verify_order_before_add(db: Session, order: Order) -> bool:

    VALID_STATUS = ["arrived", "requested", "pending"]
    
    if (not order.material_part_number) or (order.aircraft_serial_number) or (order.arrival_date) or (order.status):
        print("Missing information about aircraft!")
        return False
    
    if not str(order.status).lower in VALID_STATUS:
        print(f"Status is {order} but should be one of {VALID_STATUS}")
        return False

    aircraft = db.query(Aircraft).filter(Aircraft.serial_number == order.aircraft_serial_number).first()
    if not aircraft:
        print(f"Aircraft {order.aircraft_serial_number} is not in the database. Cannot make order for it!")
        return False

    material = db.query(Material).filter(Material.part_number == order.material_part_number).first()
    if not material:
        print(f"Material {order.material_part_number} is not in the database. Cannot make order with it!")
        return False
    
    #!!! THIS MIGHT NOT BE TRUE, DEPENDS OF THE CONTEXT, BUT WAS A FUN IDEA TO SKIP DUPLICATES
    # BETTER IDEA: EVERY ORDER TO HAVE AN ORDER-NUMBER
    existing_order = db.query(Order).filter(Order.arrival_date == order.arrival_date, Order.aircraft_serial_number == order.aircraft_serial_number, Order.material_part_number == order.material_part_number).first()
    if existing_order:
        print(f"This order is already in the database!") 
        return False

    return True