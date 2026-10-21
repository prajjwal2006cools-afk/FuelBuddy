
from fastapi import APIRouter, Query
from math import radians, sin, cos, sqrt, atan2

router = APIRouter(prefix="/api/stations", tags=["stations"])

# Demo station data. Coordinates are illustrative, not verified live listings.
MOCK_STATIONS = [
    {
        "id": 1,
        "name": "Reliance Auto",
        "lat": 12.9716,
        "lng": 77.5946,
        "price_petrol": 102.50,
        "price_diesel": 90.80,
        "amenities": ["air", "store"],
        "photo": "assets/img/hero.jpg"
    },
    {
        "id": 2,
        "name": "IndianOil Express",
        "lat": 12.9750,
        "lng": 77.5990,
        "price_petrol": 102.30,
        "price_diesel": 90.60,
        "amenities": ["restroom"],
        "photo": "assets/img/hero.jpg"
    },
    {
        "id": 3,
        "name": "Fuel Point",
        "lat": 12.9650,
        "lng": 77.5850,
        "price_petrol": 102.70,
        "price_diesel": 91.00,
        "amenities": ["air", "restroom"],
        "photo": "assets/img/hero.jpg"
    }
]


def distance_km(lat1, lng1, lat2, lng2):
    """Calculate the great-circle distance between two coordinates."""
    earth_radius_km = 6371.0

    lat1, lng1, lat2, lng2 = map(
        radians, [lat1, lng1, lat2, lng2]
    )

    dlat = lat2 - lat1
    dlng = lng2 - lng1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
    )

    return 2 * earth_radius_km * atan2(
        sqrt(a), sqrt(1 - a)
    )


@router.get("/")
def get_stations(
    lat: float = Query(12.9716, ge=-90, le=90),
    lng: float = Query(77.5946, ge=-180, le=180),
    radius_km: float = Query(5.0, gt=0, le=500)
):
    nearby = []

    for station in MOCK_STATIONS:
        distance = distance_km(
            lat,
            lng,
            station["lat"],
            station["lng"]
        )

        if distance <= radius_km:
            result = station.copy()
            result["distance_km"] = round(distance, 2)
            nearby.append(result)

    return sorted(nearby, key=lambda station: station["distance_km"])
