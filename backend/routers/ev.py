from fastapi import APIRouter
import httpx
from ..config import settings

router = APIRouter(prefix="/api/ev", tags=["ev"])

@router.get("/chargers")
async def get_chargers(lat: float = 28.6139, lng: float = 77.2090, distance: float = 10):
    if not settings.OPEN_CHARGE_MAP_API_KEY:
        # Fallback Mock Data
        return [
            {
                "id": "1",
                "name": "Tata Power EZ Charge",
                "lat": 28.6150,
                "lng": 77.2150,
                "power_kw": 30,
                "type": "DC Fast",
                "cost": "₹18/kWh"
            },
            {
                "id": "2",
                "name": "Ather Grid",
                "lat": 28.6100,
                "lng": 77.2000,
                "power_kw": 7.4,
                "type": "AC Slow",
                "cost": "₹15/kWh"
            }
        ]
        
    async with httpx.AsyncClient() as client:
        url = "https://api.openchargemap.io/v3/poi/"
        params = {
            "key": settings.OPEN_CHARGE_MAP_API_KEY,
            "latitude": lat,
            "longitude": lng,
            "distance": distance,
            "distanceunit": "KM"
        }
        res = await client.get(url, params=params)
        if res.status_code == 200:
            return res.json()
        return []
