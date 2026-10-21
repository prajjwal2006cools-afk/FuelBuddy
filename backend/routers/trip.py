from fastapi import APIRouter
from pydantic import BaseModel
import httpx
from ..config import settings
import math

router = APIRouter(prefix="/api/trip", tags=["trip"])

class TripRequest(BaseModel):
    origin: str
    destination: str
    city_mpg: float
    highway_mpg: float
    fuel_price: float
    tank_size: float = 40.0

def calculate_distance(lat1, lon1, lat2, lon2):
    # Haversine formula
    R = 6371  # Radius of earth in km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

@router.post("/calculate")
async def calculate_trip(req: TripRequest):
    distance_km = 350.0  # Default fallback
    duration_min = 240.0 # Default fallback
    
    # Attempt Geocoding
    async with httpx.AsyncClient() as client:
        try:
            res_orig = await client.get(f"https://nominatim.openstreetmap.org/search?q={req.origin}&format=json&limit=1", headers={"User-Agent": "FuelBuddyApp/1.0"})
            res_dest = await client.get(f"https://nominatim.openstreetmap.org/search?q={req.destination}&format=json&limit=1", headers={"User-Agent": "FuelBuddyApp/1.0"})
            
            if res_orig.status_code == 200 and res_dest.status_code == 200:
                orig_data = res_orig.json()
                dest_data = res_dest.json()
                
                if orig_data and dest_data:
                    lat1, lon1 = float(orig_data[0]['lat']), float(orig_data[0]['lon'])
                    lat2, lon2 = float(dest_data[0]['lat']), float(dest_data[0]['lon'])
                    
                    # Try OSRM routing if available or just use Haversine as a fallback distance
                    # For a true OSRM call without an API key (using public demo server):
                    osrm_url = f"https://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
                    res_osrm = await client.get(osrm_url)
                    if res_osrm.status_code == 200:
                        osrm_data = res_osrm.json()
                        if osrm_data.get('routes'):
                            distance_km = osrm_data['routes'][0]['distance'] / 1000.0
                            duration_min = osrm_data['routes'][0]['duration'] / 60.0
                    else:
                        distance_km = calculate_distance(lat1, lon1, lat2, lon2) * 1.2 # Multiply by 1.2 to simulate road distance
                        duration_min = (distance_km / 60.0) * 60 # Assume 60km/h avg speed
        except Exception as e:
            print(f"Routing error: {e}")
            pass
            
    # Assume 20% city driving, 80% highway driving
    avg_mpg = (req.city_mpg * 0.2) + (req.highway_mpg * 0.8)
    
    fuel_used_liters = distance_km / avg_mpg if avg_mpg > 0 else 0
    total_cost = fuel_used_liters * req.fuel_price
    co2_emitted = fuel_used_liters * 2.31  # Approx 2.31 kg CO2 per liter of petrol
    
    # Refuel Optimizer logic
    range_km = avg_mpg * req.tank_size
    refuels_needed = math.floor(distance_km / range_km) if range_km > 0 else 0
    
    refuel_recommendation = ""
    if refuels_needed > 0:
        refuel_recommendation = f"You will need to refuel approximately {refuels_needed} time(s) on this route. We recommend checking stations around {(range_km * 0.8):.0f} km into your trip."
    else:
         refuel_recommendation = "You have enough range to complete this trip without refueling!"

    return {
        "distance_km": round(distance_km, 2),
        "duration_min": round(duration_min, 2),
        "fuel_used_liters": round(fuel_used_liters, 2),
        "total_cost": round(total_cost, 2),
        "co2_emitted_kg": round(co2_emitted, 2),
        "refuels_needed": refuels_needed,
        "refuel_recommendation": refuel_recommendation
    }
