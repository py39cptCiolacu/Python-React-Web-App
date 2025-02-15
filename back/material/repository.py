from typing import List
import pandas as pd
from sqlalchemy.orm import Session
from back.models import Material

def get_all_materials(db: Session) -> List[Material]:
    materials = db.query(Material).all()
    return materials 

def create_new_materials(db: Session, file_path: str):
    print(file_path)
    materials = pd.read_excel(file_path)

    for index, row in materials.iterrows():
        new_material= Material(
            part_number = row["PN"],
            name = row["Name"],
            type = row["Type"],
            weight = row["Weight"],
        )
        db.add(new_material)

    db.commit()
    db.close()
