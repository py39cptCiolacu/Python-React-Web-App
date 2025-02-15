from typing import List
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from back.models import Material

def get_all_materials(db: Session) -> List[Material]:
    materials = db.query(Material).all()
    return materials 

def create_new_materials(db: Session, file_path: str):
    print(f"Processing file: {file_path}")
    
    try:
        materials = pd.read_excel(file_path)
    except Exception as e:
        raise Exception(f"Failed to read file: {str(e)}")
    
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
            skipped_materials.append(f"Material {new_material.part_number} skipped due to validation error!")

    if valid_new_materials:
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
    else:
        raise Exception(f"No valid materials to add. Skipped: {', '.join(skipped_materials)}")


def _verify_material_before_add(db: Session, material: Material) -> bool:

    if not all([material.name, material.part_number, material.type, material.weight]):
        print("Missing information about material!")
        return False
    
    if not all([material.name is not None, material.part_number is not None, material.type is not None, material.weight is not None]):
        print("Missing information about material!")
        return False

    existing_material = db.query(Material).filter(Material.part_number == material.part_number).first()
    if existing_material:
        print(f"{material.part_number} already in the database!")
        return False
    
    if material.weight < 0:
        print("Weight cannot be less than 0!")
        return False
    
    return True