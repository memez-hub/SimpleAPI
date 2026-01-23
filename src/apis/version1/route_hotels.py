from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx

from schemas.hotels import HotelCreate, HotelResponce, SerpSyncResponse
from db.session import get_db
from db.repository.hotels import create_new_hotel, get_hotels, upsert_hotel_from_serp
from services.serpapi import fetch_hotels

router = APIRouter()


@router.post("/", response_model=HotelResponce)
async def create_hotel(hotel: HotelCreate, db: Session = Depends(get_db)):
    new_hotel = create_new_hotel(db=db, hotel=hotel)
    return new_hotel


@router.get("/", response_model=list[HotelResponce])
async def list_hotels(db: Session = Depends(get_db)):
    hotels = get_hotels(db=db)
    return hotels


@router.post("/sync", response_model=SerpSyncResponse)
async def sync_hotels(
    city: str = "New York",
    check_in_date: date | None = None,
    check_out_date: date | None = None,
    adults: int = 2,
    currency: str = "USD",
    db: Session = Depends(get_db),
):
    try:
        hotels = fetch_hotels(
            city,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            adults=adults,
            currency=currency,
        )
    except RuntimeError as exc:
        status_code = 500 if "SERPAPI_API_KEY" in str(exc) else 502
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Serp API error {exc.response.status_code}: {exc.response.text}",
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Serp API request failed: {exc}",
        ) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Failed to fetch data from Serp API") from exc

    created = 0
    updated = 0
    for hotel_data in hotels:
        _, was_created = upsert_hotel_from_serp(db=db, hotel_data=hotel_data)
        if was_created:
            created += 1
        else:
            updated += 1

    return SerpSyncResponse(city=city, total=len(hotels), created=created, updated=updated)
