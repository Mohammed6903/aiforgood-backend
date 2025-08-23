from app.db.crud import get_nearby_donors
from typing import Any, Dict
from geopy.geocoders import Nominatim
from google.adk.tools import LongRunningFunctionTool

def fetch_nearby_donors(lng: float, lat: float, radius: float) -> list[Dict[str, Any]]:
    return get_nearby_donors(lng, lat, radius)

long_running_tool = LongRunningFunctionTool(func=fetch_nearby_donors)

def fetch_location_info(lat: float, lng: float) -> dict:
    geolocator = Nominatim(user_agent="aiforgood")
    location = geolocator.reverse((lat, lng), language='en')
    if location and location.raw and 'address' in location.raw:
        address = location.raw['address']
        return {
            "city": address.get("city") or address.get("town") or address.get("village"),
            "state": address.get("state"),
            "country": address.get("country"),
            "postcode": address.get("postcode")
        }
    return {}

long_running_tool = LongRunningFunctionTool(func=fetch_location_info)