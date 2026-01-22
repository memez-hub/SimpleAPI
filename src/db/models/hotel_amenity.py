from sqlalchemy import Column, Integer, Table, ForeignKey
from db.base import Base

hotel_amenity = Table(
    'hotel_amenity',
    Base.metadata,
    Column('hotel_id', Integer, ForeignKey('hotels.id'), primary_key=True),
    Column('amenity_id', Integer, ForeignKey('amenities.id'), primary_key=True)
)