from typing import List
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from back.models import Aircraft

def get_all_aircrafs(db: Session) -> List[Aircraft]:
    aircrafts = db.query(Aircraft).all()
    return aircrafts

def create_new_aircrafts(db: Session, file_path: str):
    print(file_path)
    aircrafts = pd.read_excel(file_path)
    valid_new_aircrafts = []

    for index, row in aircrafts.iterrows():
        new_aircraft = Aircraft(
            serial_number = row["Serial Number"],
            model = row["Model"],
            manufacturer = row["Manufacturer"],
            capacity = row["Capacity"],
            configuration = row["Configuration"]
        )

        if _verify_aircraft_before_add(db, new_aircraft):
            valid_new_aircrafts.append(new_aircraft)
        else:
            ### user error with all that failed
            print(f"Aircraft {new_aircraft.serial_number} skipped due to validation error!")

    if valid_new_aircrafts:
        try:
            db.add_all(valid_new_aircrafts)
            db.commit()
            #user info
        except IntegrityError:
            db.rollback()
            #error during databse commit
        except Exception as e:
            db.rollback()
            #unexpected error
    else:
        #inform the user - no valid enteries
        pass

def delete_aircraft():
    pass

def edit_aircraft():
    pass

def _verify_aircraft_before_add(db: Session, aircraft: Aircraft) -> bool:
    
    if (not aircraft.serial_number) or (not aircraft.capacity) or (not aircraft.configuration) or (not aircraft.manufacturer):
        print("Missing information about aircraft!")
        return False

    existing_aircraft = db.query(Aircraft).filter(Aircraft.serial_number == aircraft.serial_number).first()
    if existing_aircraft:
        print(f"{aircraft.serial_number} already in the database")
        return False

    if aircraft.capacity < 0:
        print("Capacity cannot be less than 0!")
        return False

    return True