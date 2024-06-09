from fastapi import APIRouter, HTTPException
from app.schemas.invoice import InvoiceCreate, Invoice
from app.services.invoice_service import create_invoice, get_invoice

router = APIRouter()

@router.post("/invoice", response_model=Invoice)
def create_invoice_endpoint(invoice: InvoiceCreate):
    return create_invoice(invoice)

@router.get("/invoice/{id}", response_model=Invoice)
def get_invoice_endpoint(id: str):
    invoice = get_invoice(id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice
