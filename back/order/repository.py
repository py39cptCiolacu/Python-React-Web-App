from typing import List
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from back.models import Order, Aircraft, Material

def get_all_orders(db: Session) -> List[Order]:
    orders = db.query(Order).all()
    return orders

def create_new_orders(db: Session, file_path: str):
    print(f"Processing file: {file_path}")
    
    try:
        orders = pd.read_excel(file_path)
    except Exception as e:
        raise Exception(f"Failed to read file: {str(e)}")
    
    valid_orders = []
    skipped_orders = []

    for index, row in orders.iterrows():
        new_order = Order(
            aircraft_serial_number=row["Aircraft Serial Number"],
            material_part_number=row["Material PN"],
            arrival_date=row["Arrival Date"],
            status=row["Status"],
        )

        if _verify_order_before_add(db, new_order):
            valid_orders.append(new_order)
        else:
            skipped_orders.append(f"Order for aircraft {new_order.aircraft_serial_number} with material {new_order.material_part_number} skipped due to validation error!")

    if valid_orders:
        try:
            db.add_all(valid_orders)
            db.commit()
            return {"success": True, "message": f"{len(valid_orders)} orders added successfully!"}
        except IntegrityError as e:
            db.rollback()
            raise Exception(f"Database integrity error: {str(e)}")
        except Exception as e:
            db.rollback()
            raise Exception(f"Unexpected error during commit: {str(e)}")
    else:
        raise Exception(f"No valid orders to add. Skipped: {', '.join(skipped_orders)}")

def _verify_order_before_add(db: Session, order: Order) -> bool:

    VALID_STATUS = ["arrived", "requested", "pending"]
    
    if not all([order.material_part_number, order.aircraft_serial_number, order.arrival_date, order.status]):
        print("Missing information about order!")
        return False
    
    if not all([order.material_part_number is not None, order.aircraft_serial_number is not None, order.arrival_date is not None, order.status is not None]):
        print("Missing information about order!")
        return False
    
    if not str(order.status).lower() in VALID_STATUS:
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