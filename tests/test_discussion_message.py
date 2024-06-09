from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_discussion_message():
    response = client.post("/discussion_message", json={
        "MessageId": "789",
        "PsychologistId": "456",
        "PatientId": "123",
        "Message": "Hello, how are you?",
        "Timestamp": "2023-01-01T12:00:00Z",
        "Sender": "Patient",
        "Seen": False
    })
    assert response.status_code == 200
    assert response.json()["MessageId"] == "789"

def test_get_discussion_message():
    response = client.get("/discussion_message/456/123")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["MessageId"] == "789"
