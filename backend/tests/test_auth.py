from fastapi.testclient import TestClient
from backend.main import app
from backend.models.db import init_db

# Initialize DB for tests
init_db()
client = TestClient(app)

def test_send_otp():
    response = client.post("/api/auth/send-otp", json={"phone_number": "+919999999999"})
    assert response.status_code == 200
    assert response.json()["message"] == "OTP sent successfully"

def test_send_otp_invalid_phone():
    response = client.post("/api/auth/send-otp", json={"phone_number": "123"})
    assert response.status_code == 400
