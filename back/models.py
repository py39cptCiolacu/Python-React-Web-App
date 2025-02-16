from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
# from back.utils.base import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Aircraft(Base):
    __tablename__ = "aircraft"

    serial_number = Column(String, primary_key=True)
    model = Column(String)
    manufacturer = Column(String)
    capacity = Column(Integer)
    configuration = Column(Integer)

    orders = relationship("Order", back_populates="aircraft")

class Material(Base):
    __tablename__ = "material"

    part_number = Column(String, primary_key = True)
    name = Column(String)
    type = Column(String)
    weight = Column(Integer)

    orders = relationship("Order", back_populates="material")

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    aircraft_serial_number = Column(String, ForeignKey("aircraft.serial_number"))
    material_part_number = Column(String, ForeignKey("material.part_number"))
    arrival_date = Column(DateTime)
    status = Column(String)
    
    aircraft = relationship("Aircraft", back_populates="orders")
    material = relationship("Material", back_populates="orders")