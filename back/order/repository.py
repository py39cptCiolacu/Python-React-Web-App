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
    ACCEPTED_EXTENSIONS = ["xlsx", "xls", "csv"]
    file_extension = file_path.filename.rsplit('.', 1)[1].lower()

    if file_extension not in ACCEPTED_EXTENSIONS:
        raise Exception(f"This applications allow only Excel and CSV files!")
    
    try:
        if file_extension in ["xlsx", "xls"]:
            orders = pd.read_excel(file_path)
        elif file_extension == "csv":
            orders = pd.read_csv(file_path)   
    except Exception as e:
        raise Exception(f"Failed to read file: {str(e)}")

    valid_orders, skipped_orders = _check_for_valid_orders(orders, db)

    if not valid_orders:
        raise Exception("No valid orders provieded in the file!")
    
    return _commit_valid_orders(valid_orders, skipped_orders, db)

def _check_for_valid_orders(orders: pd.DataFrame, db: Session) -> tuple[list, list]:
    expected_columns = ["aircraft serial number", "material pn", "arrival date", "status"]
    orders.columns.str.lower()
    
    missing_columns = [col for col in expected_columns if col.lower() not in orders.columns.str.lower()]

    if missing_columns:
        raise Exception(f"The files is missing columns: {missing_columns}")

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

    return valid_orders, skipped_orders

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

def _commit_valid_orders(valid_orders: list, skipped_orders: list, db: Session):
    if not valid_orders:
        raise Exception(f"No valid orders to add. Skipped: {', '.join(skipped_orders)}")
    
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