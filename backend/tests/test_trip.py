from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_trip_calculation():
    response = client.post("/api/trip/calculate", json={
        "origin": "Mumbai",
        "destination": "Pune",
        "city_mpg": 10.0,
        "highway_mpg": 15.0,
        "fuel_price": 100.0,
        "tank_size": 40.0
    })
    assert response.status_code == 200
    data = response.json()
    assert "total_cost" in data
    assert "fuel_used_liters" in data
    assert "refuel_recommendation" in data
