from typing import List
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from back.models import Aircraft
import logging

def get_all_aircrafs(db: Session) -> List[Aircraft]:
    aircrafts = db.query(Aircraft).all()
    return aircrafts

def get_aircraft_by_serial_number(db: Session, serial_number: str) -> Aircraft:

    aircraft = db.query(Aircraft).filter(Aircraft.serial_number == serial_number).first()
    if aircraft:
        return aircraft
    else:
        raise NoResultFound(f"Aircraft {serial_number} was not found in the databse!")

def create_new_aircrafts(db: Session, file_path):
    print(f"Processing file: {file_path}")
    ACCEPTED_EXTENSIONS = ["xlsx", "xls", "csv"]
    file_extension = file_path.filename.rsplit('.', 1)[1].lower()
    
    if file_extension not in ACCEPTED_EXTENSIONS:
        logging.error("Incorrect type of file uploaded!")
        raise Exception(f"This applications allow only Excel and CSV files!")
    
    try:
        if file_extension in ["xlsx", "xls"]:
            aircrafts = pd.read_excel(file_path)
        elif file_extension == "csv":
            aircrafts = pd.read_csv(file_path)   
    except Exception as e:
        logging.error("Backend failed to read the file!")
        raise Exception(f"Failed to read file: {str(e)}")

    valid_new_aircrafts, skipped_aircrafts = _check_for_valid_aircrafts(aircrafts, db)
    if not valid_new_aircrafts:
        logging.warning("No valid aircrafts were found in file!")
        raise Exception("No valid aircrafts were provieded in the file!")

    return _commit_valid_aircrafts(valid_new_aircrafts, skipped_aircrafts, db)

def _check_for_valid_aircrafts(aircrafts: pd.DataFrame, db: Session) -> tuple[list, list]: 
    expected_columns = ["serial number", "model", "manufacturer", "configuration"]
    aircrafts.columns.str.lower()
    
    missing_columns = [col for col in expected_columns if col.lower() not in aircrafts.columns.str.lower()]

    if missing_columns:
        logging.warning(f"Uploaded file have missing columns: {missing_columns}")
        raise Exception(f"The files is missing columns: {missing_columns}")

    skipped_aircrafts = []
    valid_new_aircrafts = []

    for _, row in aircrafts.iterrows():
        new_aircraft = Aircraft(
            serial_number=row["Serial Number"],
            model=row["Model"],
            manufacturer=row["Manufacturer"],
            capacity=row["Capacity"],
            configuration=row["Configuration"]
        )

        if _verify_aircraft_before_add(db, new_aircraft):
            valid_new_aircrafts.append(new_aircraft)
        else:
            logging.warning(f"Aircraft {new_aircraft.serial_number} skipped due to validation error!")
            skipped_aircrafts.append(f"Aircraft {new_aircraft.serial_number} skipped due to validation error!")
    
    return valid_new_aircrafts, skipped_aircrafts

def _verify_aircraft_before_add(db: Session, aircraft: Aircraft) -> bool:
    
    if not all([aircraft.serial_number, aircraft.capacity, aircraft.configuration, aircraft.manufacturer]):
        logging.warning("Missing information about aircraft!")
        return False
    
    if not all([aircraft.serial_number is not None, aircraft.capacity is not None, aircraft.configuration is not None, aircraft.manufacturer is not None]):
        logging.warning("Missing information about aircraft!")
        return False

    existing_aircraft = db.query(Aircraft).filter(Aircraft.serial_number == aircraft.serial_number).first()
    if existing_aircraft:
        logging.warning(f"{aircraft.serial_number} already in the database")
        return False

    if aircraft.capacity < 0:
        logging.warning(f"{aircraft.serial_number} - Capacity cannot be less than 0!")
        return False

    logging.info(f"Aircraft {aircraft.serial_number} passed all checks!")
    return True

def _commit_valid_aircrafts(valid_new_aircrafts: list, skipped_aircrafts: list, db: Session):

    if not valid_new_aircrafts:
        raise Exception(f"No valid aircrafts to add. Skipped: {', '.join(skipped_aircrafts)}")
    
    try:
        db.add_all(valid_new_aircrafts)
        db.commit()
        return {"success": True, "message": f"{len(valid_new_aircrafts)} aircrafts added successfully!"}
    except IntegrityError as e:
        db.rollback()
        raise Exception(f"Database integrity error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise Exception(f"Unexpected error during commit: {str(e)}")
