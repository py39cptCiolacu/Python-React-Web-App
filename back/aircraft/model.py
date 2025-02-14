from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from back.utils.base import Base

class Aircraft(Base):
    __tablename__ = "aircraft"

    serial_number = Column(String, primary_key=True)
    model = Column(String)
    manufacturer = Column(String)
    capacity = Column(Integer)
    configuration = Column(Integer)

    orders = relationship("Order", back_populates="aircraft")