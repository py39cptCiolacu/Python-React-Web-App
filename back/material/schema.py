from pydantic import BaseModel

class MaterialSchema(BaseModel):
    part_number: str
    name: str
    type: str
    weight: int

    class Config:
        from_attributes = True