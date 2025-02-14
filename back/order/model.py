from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from back.utils.base import Base

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    aircraft_serial_number = Column(String, ForeignKey("aircraft.serial_number"))
    material_part_number = Column(String, ForeignKey("material.part_number"))
    arrival_date = Column(String)
    status = Column(String)
    
    aircraft = relationship("Aircraft", back_populates="orders")
    material = relationship("Material", back_populates="orders")