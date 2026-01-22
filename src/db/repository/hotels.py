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


def get_hotels(db: Session):
    return db.query(Hotel).all()