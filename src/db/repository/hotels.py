from sqlalchemy.orm import Session
from db.models.amenity import Amenity
from schemas.hotels import HotelCreate
from db.models.hotel import Hotel


def create_new_hotel(db: Session, hotel: HotelCreate):
    hotel_obj = Hotel(
        name=hotel.name,
        location=hotel.location,
        price_per_night=hotel.price_per_night,
        rating=hotel.rating,
        image_url=hotel.image_url,
        lattitude=hotel.lattitude,
        longitude=hotel.longitude,
        description=hotel.description,
    )

    db.add(hotel_obj)
    db.flush()  # 👈 get hotel.id

    for amenity_name in hotel.amenities:
        amenity = db.query(Amenity).filter(
            Amenity.name == amenity_name
        ).first()

        if not amenity:
            amenity = Amenity(name=amenity_name)
            db.add(amenity)
            db.flush()

        hotel_obj.amenities.append(amenity)

    db.commit()
    db.refresh(hotel_obj)

    return hotel_obj



def upsert_hotel_from_serp(db: Session, hotel_data: dict) -> tuple[Hotel, bool]:
    name = hotel_data.get("name")
    location = hotel_data.get("location")
    if not name or not location:
        raise ValueError("Hotel name and location are required")

    existing_hotel = (
        db.query(Hotel)
        .filter(Hotel.name == name, Hotel.location == location)
        .first()
    )

    created = False
    if existing_hotel:
        existing_hotel.price_per_night = hotel_data.get("price_per_night")
        existing_hotel.rating = hotel_data.get("rating")
        existing_hotel.image_url = hotel_data.get("image_url")
        existing_hotel.lattitude = hotel_data.get("lattitude")
        existing_hotel.longitude = hotel_data.get("longitude")
        existing_hotel.description = hotel_data.get("description")
        hotel_obj = existing_hotel
    else:
        hotel_obj = Hotel(
            name=name,
            location=location,
            price_per_night=hotel_data.get("price_per_night"),
            rating=hotel_data.get("rating"),
            image_url=hotel_data.get("image_url"),
            lattitude=hotel_data.get("lattitude"),
            longitude=hotel_data.get("longitude"),
            description=hotel_data.get("description"),
        )
        db.add(hotel_obj)
        db.flush()
        created = True

    amenity_names = [
        amenity
        for amenity in hotel_data.get("amenities", [])
        if isinstance(amenity, str) and amenity
    ]
    if amenity_names:
        existing_amenities = {amenity.name for amenity in hotel_obj.amenities}
        for amenity_name in amenity_names:
            if amenity_name in existing_amenities:
                continue
            amenity = db.query(Amenity).filter(Amenity.name == amenity_name).first()
            if not amenity:
                amenity = Amenity(name=amenity_name)
                db.add(amenity)
                db.flush()
            hotel_obj.amenities.append(amenity)

    db.commit()
    db.refresh(hotel_obj)

    return hotel_obj, created


def get_hotels(db: Session):
    return db.query(Hotel).all()
