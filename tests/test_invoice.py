from fastapi.testclient import TestClient
from app.main import app
from decimal import Decimal

client = TestClient(app)


def test_create_invoice():
    response = client.post("/invoice", json={
        "InvoiceId": "151617",
        'PsychologistId': "456",
        'PatientId': "123",
        'ConsultationId': "101112",
        "Status": "Not Paid",
        "Amount": str(Decimal("100.0")),  # Ensure using Decimal for Amount
        "PaymentLink": "https://payment.example.com",
        "PDF": "https://example.com/invoice.pdf"
    })
    assert response.status_code == 200
    assert response.json()["InvoiceId"] == "151617"


def test_get_invoice():
    response = client.get("/invoice/151617")
    assert response.status_code == 200
    assert response.json()["InvoiceId"] == "151617"

def test_get_invoices_by_psychologist():
    response = client.get("/invoices/psychologist/456")
    assert response.status_code == 200
    assert response.json()[0]["PatientId"] == "123"
    assert response.json()[0]["PsychologistId"] == "456"
    assert response.json()[0]["InvoiceId"] == "151617"

def test_get_invoices_by_psychologist_patient():
    response = client.get("/invoices/456/123")
    assert response.status_code == 200
    assert response.json()[0]["PatientId"] == "123"
    assert response.json()[0]["PsychologistId"] == "456"
    assert response.json()[0]["InvoiceId"] == "151617"
