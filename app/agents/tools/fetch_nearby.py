from app.db.crud import get_nearby_donors
from typing import Any, Dict
from geopy.geocoders import Nominatim
from google.adk.tools import FunctionTool
from app.db.session import prisma, Prisma

async def fetch_nearby_donors(lat: float, lng: float, radius: float) -> list[Dict[str, Any]]:
    print("finding")
    if not prisma.is_connected():
        await prisma.connect()
    return await get_nearby_donors(lng, lat, radius, db=prisma)

function_tool = FunctionTool(func=fetch_nearby_donors)

def fetch_location_info(lat: float, lng: float) -> dict:
    geolocator = Nominatim(user_agent="aiforgood")
    location = geolocator.reverse((lat, lng), language='en')
    print("Finding")
    if location and location.raw and 'address' in location.raw:
        address = location.raw['address']
        return {
            "city": address.get("city") or address.get("town") or address.get("village"),
            "state": address.get("state"),
            "country": address.get("country"),
            "postcode": address.get("postcode")
        }
    return {}

function_tool = FunctionTool(func=fetch_location_info)