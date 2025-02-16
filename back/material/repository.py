from typing import List
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from back.models import Material
import logging

def get_all_materials(db: Session) -> List[Material]:
    materials = db.query(Material).all()
    return materials

def get_material_by_part_number(db: Session, part_number: str) -> Material:
    material = db.query(Material).filter(Material.part_number == part_number).first()
    if material:
        return material
    else:
        raise NoResultFound(f"Material {part_number} was not found in database!")

def create_new_materials(db: Session, file_path: str) -> dict:
    print(f"Processing file: {file_path}")
    ACCEPTED_EXTENSIONS = ["xlsx", "xls", "csv"]
    file_extension = file_path.filename.rsplit('.', 1)[1].lower()
    
    if file_extension not in ACCEPTED_EXTENSIONS:
        logging.error("Incorrect type of file uploaded!")
        raise Exception(f"This applications allow only Excel and CSV files!")

    try:
        if file_extension in ["xlsx", "xls"]:
            materials = pd.read_excel(file_path)
        elif file_extension == "csv":
            materials = pd.read_csv(file_path)   
    except Exception as e:
        logging.error("Backend failed to read the file!")
        raise Exception(f"Failed to read file: {str(e)}")
    
    valid_new_materials, skipped_materials = _check_for_valid_materials(materials, db)

    if not valid_new_materials:
        raise Exception("No valid materials were provieded in the file!")

    return _commit_valid_materials(valid_new_materials, skipped_materials, db)

def _check_for_valid_materials(materials: pd.DataFrame, db: Session) -> tuple[list, list]:
    expected_columns = ["name", "type", "pn", "weight"]
    materials.columns.str.lower()

    missing_columns = [col for col in expected_columns if col.lower() not in materials.columns.str.lower()]

    if missing_columns:
        logging.warning(f"The files is missing columns: {missing_columns}")
        raise Exception(f"The files is missing columns: {missing_columns}")

    valid_new_materials = []
    skipped_materials = []

    for index, row in materials.iterrows():
        new_material = Material(
            part_number=row["PN"],
            name=row["Name"],
            type=row["Type"],
            weight=row["Weight"],
        )

        if _verify_material_before_add(db, new_material):
            valid_new_materials.append(new_material)
        else:
            logging.info(f"Material {new_material.part_number} skipped due to validation error!")
            skipped_materials.append(f"Material {new_material.part_number} skipped due to validation error!")

    return valid_new_materials, skipped_materials

def _verify_material_before_add(db: Session, material: Material) -> bool:

    if not all([material.name, material.part_number, material.type, material.weight]):
        logging.warning("Missing information about material!")
        return False
    
    if not all([material.name is not None, material.part_number is not None, material.type is not None, material.weight is not None]):
        logging.warning("Missing information about material!")
        return False

    existing_material = db.query(Material).filter(Material.part_number == material.part_number).first()
    if existing_material:
        logging.warning(f"{material.part_number} already in the database!")
        return False
    
    if material.weight < 0:
        logging.warn(f"{material.part_number} Weight cannot be less than 0!")
        return False
    
    return True

def _commit_valid_materials(valid_new_materials: list, skipped_materials: list, db: Session):
    if not valid_new_materials:
        raise Exception(f"No valid materials to add. Skipped: {', '.join(skipped_materials)}")
    
    try:
        db.add_all(valid_new_materials)
        db.commit()
        return {"success": True, "message": f"{len(valid_new_materials)} materials added successfully!"}
    except IntegrityError as e:
        db.rollback()
        raise Exception(f"Database integrity error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise Exception(f"Unexpected error during commit: {str(e)}")