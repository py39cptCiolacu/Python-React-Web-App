from sqlalchemy import Column, String
from back.utils.base import Base

class Revision(Base):
    __tablename__ = "revision"
    name = Column(String, primary_key=True)

