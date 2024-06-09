from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_patient():
    response = client.post("/patient", json={
        "PatientId": "123",
        "FirstName": "John",
        "LastName": "Doe",
        "DateOfBirth": "1990-01-01",
        "Sex": "Male",
        "Email": "john.doe@example.com",
        "PhoneNumber": "1234567890",
        "Address": {
            "street": "123 Main St",
            "number": "1",
            "postal_code": "12345",
            "city": "Anytown",
            "country": "Country"
        },
        "Description": "A test patient",
        "Photo": "https://example.com/photo.jpg",
        "PsychologistId": "456"
    })
    assert response.status_code == 200
    assert response.json()["PatientId"] == "123"

def test_get_patient():
    response = client.get("/patient/123")
    assert response.status_code == 200
    assert response.json()["PatientId"] == "123"

def test_get_patients_by_psychologist():
    response = client.get("/patients/psychologist/456")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["PatientId"] == "123"
