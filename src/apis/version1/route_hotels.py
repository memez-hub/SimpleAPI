from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.hotels import HotelCreate, HotelResponce
from db.session import get_db
from db.repository.hotels import create_new_hotel, get_hotels

router = APIRouter()

@router.post("/", response_model=HotelResponce)
async def create_hotel(hotel: HotelCreate, db: Session = Depends(get_db)):
    new_hotel = create_new_hotel(db=db, hotel=hotel)
    return new_hotel

@router.get("/", response_model=list[HotelResponce])
async def list_hotels(db: Session = Depends(get_db)):
    hotels = get_hotels(db=db)
    return hotels