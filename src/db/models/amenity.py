from db.models import hotel_amenity
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from db.base import Base



class Amenity(Base):
    __tablename__ = "amenities"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    hotels = relationship(
        "Hotel",
        secondary=lambda: hotel_amenity,
        back_populates="amenities",
        lazy="joined",
    )