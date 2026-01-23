from pydantic import BaseModel, Field
from typing import List, Optional

from schemas.amenity import AmenityResponce


class HotelCreate(BaseModel):
    name: str = Field(..., max_length=255)
    location: str = Field(..., max_length=255)
    price_per_night: Optional[int] = Field(None)
    rating: Optional[str] = Field(None)
    image_url: Optional[str] = Field(None)
    lattitude: Optional[str] = Field(None)
    longitude: Optional[str] = Field(None)
    description: str = Field(...)
    amenities: List[str] = []


class HotelResponce(BaseModel):
    id: int
    name: str
    location: str
    price_per_night: Optional[int]
    rating: Optional[str]
    image_url: Optional[str]
    lattitude: Optional[str]
    longitude: Optional[str]
    description: str
    amenities: List[AmenityResponce] = []

    class Config:
        orm_mode = True


class SerpSyncResponse(BaseModel):
    city: str
    total: int
    created: int
    updated: int
