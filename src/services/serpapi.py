import os
from typing import Any, Dict, List

import httpx

SERPAPI_URL = "https://serpapi.com/search.json"
DEFAULT_TIMEOUT = httpx.Timeout(30.0)


def _extract_properties(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    for key in ("properties", "hotels", "properties_results", "results"):
        value = data.get(key)
        if isinstance(value, list):
            return value
    return []


def _extract_price_per_night(property_data: Dict[str, Any]) -> int | None:
    rate_info = property_data.get("rate_per_night")
    if isinstance(rate_info, dict):
        extracted = rate_info.get("extracted_lowest") or rate_info.get("extracted")
        if isinstance(extracted, (int, float)):
            return int(extracted)
    price = property_data.get("price")
    if isinstance(price, (int, float)):
        return int(price)
    return None


def _extract_rating(property_data: Dict[str, Any]) -> int | None:
    rating = property_data.get("overall_rating") or property_data.get("rating")
    if isinstance(rating, (int, float)):
        return int(round(rating))
    return None


def _extract_image_url(property_data: Dict[str, Any]) -> str | None:
    for key in ("thumbnail", "image", "image_url"):
        value = property_data.get(key)
        if isinstance(value, str):
            return value
    images = property_data.get("images")
    if isinstance(images, list) and images:
        first = images[0]
        if isinstance(first, str):
            return first
        if isinstance(first, dict):
            url = first.get("thumbnail") or first.get("image")
            if isinstance(url, str):
                return url
    return None


def normalize_hotel(property_data: Dict[str, Any], city: str) -> Dict[str, Any]:
    gps = property_data.get("gps_coordinates") or {}
    latitude = gps.get("latitude")
    longitude = gps.get("longitude")
    return {
        "name": property_data.get("name") or property_data.get("title") or "",
        "location": property_data.get("address") or property_data.get("location") or city,
        "price_per_night": _extract_price_per_night(property_data),
        "rating": _extract_rating(property_data),
        "image_url": _extract_image_url(property_data),
        "lattitude": str(latitude) if latitude is not None else None,
        "longitude": str(longitude) if longitude is not None else None,
        "description": property_data.get("description") or property_data.get("snippet") or "",
        "amenities": property_data.get("amenities") or [],
    }


def fetch_hotels(city: str) -> List[Dict[str, Any]]:
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise RuntimeError("SERPAPI_API_KEY is not configured")

    params = {
        "engine": "google_hotels",
        "q": f"hotels in {city}",
        "api_key": api_key,
    }

    with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
        response = client.get(SERPAPI_URL, params=params)
        response.raise_for_status()

    data = response.json()
    hotels = _extract_properties(data)
    if not hotels and "error" in data:
        raise RuntimeError(f"Serp API error: {data.get('error')}")
    return [normalize_hotel(hotel, city) for hotel in hotels]
