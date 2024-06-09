from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_consultation():
    response = client.post("/consultation", json={
        "ConsultationId": "101112",
        "PsychologistId": "456",
        "PatientId": "123",
        "DateTime": "2023-01-15T10:00:00Z",
        "GoogleMeetLink": "https://meet.google.com/example",
        "Status": "Scheduled",
        "InvoiceId": "121314"
    })
    assert response.status_code == 200
    assert response.json()["ConsultationId"] == "101112"

def test_get_consultation():
    response = client.get("/consultation/456/123")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["ConsultationId"] == "101112"
