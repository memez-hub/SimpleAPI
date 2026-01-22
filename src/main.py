from fastapi import FastAPI
from db.base import Base 
from db.session import engine
from apis.base import api_router
import db.models.hotel  # ensure models are imported for table creation
import db.models.amenity  # ensure models are imported for table creation
import db.models.hotel_amenity  # ensure association table is imported


def include_router(app):
    app.include_router(api_router)

def create_tables():
    Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI()
    include_router(app)
    create_tables()
    return app

app = start_application()