from typing import List
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from back.models import Material

def get_all_materials(db: Session) -> List[Material]:
    materials = db.query(Material).all()
    return materials 

def create_new_materials(db: Session, file_path: str):
    print(file_path)
    materials = pd.read_excel(file_path)
    valid_new_materials = []

    for index, row in materials.iterrows():
        new_material= Material(
            part_number = row["PN"],
            name = row["Name"],
            type = row["Type"],
            weight = row["Weight"],
        )

        if _verify_material_before_add(db, new_material):
            valid_new_materials.append(new_material)
        else:
            ### user error with all that failed
            print(f"Material {new_material.part_number} skipped due to validation error!")

    if valid_new_materials:
        try:
            db.add_all(valid_new_materials)
            db.commit()
            #user info
        except IntegrityError:
            db.rollback()
            #error during databse commit
        except Exception as e:
            db.rollback()
            #unexpected error
    else:
        #inform user - not valid entires
        pass

def _verify_material_before_add(db: Session, material: Material) -> bool:

    if (not material.name) or (not material.part_number) or (not material.type) or (not material.weight):
        print("Missing information about material!")
        return False
    
    existing_material = db.query(Material).filter(Material.part_number == material.part_number).first()
    if existing_material:
        print(f"{material.part_number} already in the database!")
        return False
    
    if material.weight < 0:
        print("Weight cannot be less than 0!")
        return False