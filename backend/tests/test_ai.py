from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_predict_consumption():
    response = client.post("/api/ai/predict-consumption", json={
        "engine_size": 2.0,
        "weight_kg": 1500.0,
        "year": 2020,
        "is_highway": True
    })
    assert response.status_code == 200
    data = response.json()
    assert "predicted_kml" in data

def test_price_forecast():
    response = client.get("/api/ai/price-forecast")
    assert response.status_code == 200
    data = response.json()
    assert data["trend"] in ["up", "down", "stable"]

def test_recommend():
    response = client.post("/api/ai/recommend", json={
        "engine_size": 2.0,
        "year": 2020
    })
    assert response.status_code == 200
    data = response.json()
    assert "recommended_grade" in data
