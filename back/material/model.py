from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from back.utils.base import Base


class Material(Base):
    __tablename__ = "material"

    part_number = Column(String, primary_key = True)
    name = Column(String)
    type = Column(String)
    weight = Column(Integer)

    orders = relationship("Order", back_populates="material")
