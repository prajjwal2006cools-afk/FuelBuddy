from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    vehicles = relationship("Vehicle", back_populates="owner")
    trips = relationship("Trip", back_populates="owner")

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    trim = Column(String)
    fuel_type = Column(String)
    fuel_grade = Column(String)
    tank_size = Column(Float)
    city_mpg = Column(Float)
    highway_mpg = Column(Float)
    is_default = Column(Boolean, default=False)

    owner = relationship("User", back_populates="vehicles")

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    origin = Column(String)
    destination = Column(String)
    distance_km = Column(Float)
    duration_min = Column(Float)
    cost = Column(Float)
    fuel_used = Column(Float)
    co2_emitted = Column(Float)

    owner = relationship("User", back_populates="trips")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
