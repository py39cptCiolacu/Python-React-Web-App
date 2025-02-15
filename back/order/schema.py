from pydantic import BaseModel
from datetime import datetime

class OrderSchema(BaseModel):
    material_part_number: str
    aircraft_serial_number: str
    arrival_date: datetime
    status: str

    class Config:
        from_attributes = True
