from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    phone_number: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    name: Optional[str] = None
    class Config:
        from_attributes = True

class VehicleBase(BaseModel):
    make: str
    model: str
    year: int
    trim: str
    fuel_type: str
    fuel_grade: str
    tank_size: float
    city_mpg: float
    highway_mpg: float
    is_default: bool = False

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True

class TripBase(BaseModel):
    origin: str
    destination: str
    distance_km: float
    duration_min: float
    cost: float
    fuel_used: float
    co2_emitted: float

class TripCreate(TripBase):
    pass

class Trip(TripBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True
