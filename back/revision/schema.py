from pydantic import BaseModel

class RevisionSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True