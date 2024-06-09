from fastapi.testclient import TestClient
from app.main import app
from decimal import Decimal

client = TestClient(app)


def test_create_invoice():
    response = client.post("/invoice", json={
        "InvoiceId": "151617",
        "Status": "Not Paid",
        "Amount": str(Decimal("100.0")),  # Ensure using Decimal for Amount
        "PaymentLink": "http://payment.example.com",
        "PDF": "http://example.com/invoice.pdf"
    })
    assert response.status_code == 200
    assert response.json()["InvoiceId"] == "151617"


def test_get_invoice():
    # Ensure the invoice exists before retrieving
    client.post("/invoice", json={
        "InvoiceId": "151617",
        "Status": "Not Paid",
        "Amount": str(Decimal("100.0")),
        "PaymentLink": "http://payment.example.com",
        "PDF": "http://example.com/invoice.pdf"
    })

    response = client.get("/invoice/151617")
    assert response.status_code == 200
    assert response.json()["InvoiceId"] == "151617"
