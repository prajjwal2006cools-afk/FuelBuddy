from fastapi import APIRouter

router = APIRouter(prefix="/api/fuel", tags=["fuel"])

FUEL_METADATA = [
    {
        "type": "Petrol (Gasoline)",
        "density": "0.74 kg/L at 15°C",
        "energy": "34.2 MJ/L",
        "co2": "2.31 kg/L",
        "description": "Standard fuel for most passenger cars.",
        "grades": ["Regular (87/91 RON)", "Premium (95 RON)", "High-Octane (98+ RON)"]
    },
    {
        "type": "Diesel",
        "density": "0.83-0.85 kg/L at 15°C",
        "energy": "38.6 MJ/L",
        "co2": "2.68 kg/L",
        "description": "Used for heavy-duty vehicles and many SUVs/trucks. Higher energy density than petrol.",
        "grades": ["Standard Diesel", "Premium/Turbo Diesel"]
    },
    {
        "type": "CNG",
        "density": "0.128 kg/m³ (Gas)",
        "energy": "38 MJ/m³",
        "co2": "~2.0 kg/kg",
        "description": "Compressed Natural Gas. Cheaper and burns cleaner, but requires heavy tanks.",
        "grades": ["Standard CNG"]
    },
    {
        "type": "EV (Electricity)",
        "density": "N/A",
        "energy": "3.6 MJ/kWh",
        "co2": "Depends on local grid (0 to ~0.9 kg/kWh)",
        "description": "Electric power. Most efficient and cost-effective per km.",
        "grades": ["AC Slow (3-22 kW)", "DC Fast (50-350+ kW)"]
    }
]

@router.get("/metadata")
def get_fuel_metadata():
    return FUEL_METADATA
