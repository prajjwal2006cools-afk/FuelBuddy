from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models.db import get_db, Vehicle, User
from ..schemas import Vehicle as VehicleSchema, VehicleCreate
from .auth import get_current_user

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])

@router.get("/", response_model=List[VehicleSchema])
def get_vehicles(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user.vehicles

@router.post("/", response_model=VehicleSchema)
def create_vehicle(vehicle: VehicleCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if vehicle.is_default:
        # Reset other default vehicles
        for v in current_user.vehicles:
            v.is_default = False
            
    db_vehicle = Vehicle(**vehicle.model_dump(), owner_id=current_user.id)
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@router.delete("/{vehicle_id}")
def delete_vehicle(vehicle_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id, Vehicle.owner_id == current_user.id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    db.delete(vehicle)
    db.commit()
    return {"message": "Vehicle deleted"}
