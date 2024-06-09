from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_psychologist():
    response = client.post("/psychologist", json={
        "PsychologistId": "456",
        "FirstName": "Jane",
        "LastName": "Smith",
        "DateOfBirth": "1980-02-02",
        "Sex": "Female",
        "Photo": "https://example.com/photo.jpg"
    })
    assert response.status_code == 200
    assert response.json()["PsychologistId"] == "456"

def test_get_psychologist():
    response = client.get("/psychologist/456")
    assert response.status_code == 200
    assert response.json()["PsychologistId"] == "456"
