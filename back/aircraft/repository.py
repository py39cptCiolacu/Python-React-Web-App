from typing import List
import pandas as pd
from sqlalchemy.orm import Session
from back.models import Aircraft

def get_all_aircrafs(db: Session) -> List[Aircraft]:
    aircrafts = db.query(Aircraft).all()
    return aircrafts

def create_new_aircrafts(db: Session, file_path: str):
    print(file_path)
    aircrafts = pd.read_excel(file_path)

    for index, row in aircrafts.iterrows():
        new_aircraft = Aircraft(
            serial_number = row["Serial Number"],
            model = row["Model"],
            manufacturer = row["Manufacturer"],
            capacity = row["Capacity"],
            configuration = row["Configuration"]
        )
        db.add(new_aircraft)

    db.commit()
    db.close()

def delete_aircraft():
    pass

def edit_aircraft():
    pass
