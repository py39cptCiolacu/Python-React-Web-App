from pydantic import BaseModel

class AircraftSchema(BaseModel):
    serial_number: str
    model: str
    manufacturer: str
    capacity: int
    configuration: int
    
    class Config:
        from_attributes = True