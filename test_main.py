from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_post_credit_score():
    data = {
        "age": "16-25",
        "gender": "male",
        "driving_experience": "0-9y",
        "education": "none",
        "income": "poverty",
        "vehicle_year": "before 2015",
        "vehicle_type": "sedan",
        "annual_mileage": 16000.0
    }
    response = client.post("/credit_score", data={k: (v if isinstance(v, str) else float(v)) for k, v in data.items()})
    assert response.status_code == 200
    assert "credit_score" in response.json()

def test_get_credit_score():
    response = client.post("/credit_score")
    assert response.status_code == 422  # The endpoint expects form data, not JSON