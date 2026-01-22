from fastapi import APIRouter

from apis.version1 import route_hotels

api_router = APIRouter()

api_router.include_router(route_hotels.router, prefix="/hotels", tags=["hotels"])