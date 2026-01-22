from db.models import hotel_amenity
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    price_per_night = Column(Integer, nullable=True)
    rating = Column(Integer, nullable=True)
    image_url = Column(String, nullable=True)
    lattitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    description = Column(String)

    amenities = relationship(
        "Amenity",
        secondary=lambda: hotel_amenity,
        back_populates="hotels",
        lazy="joined"
    )