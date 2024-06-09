import logging
from fastapi import APIRouter, HTTPException
from app.schemas.invoice import InvoiceCreate, Invoice
from app.services.invoice_service import (create_invoice, get_invoice, get_invoices_by_psychologist,
                                          get_invoices_by_psychologist_patient)

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/invoice", response_model=Invoice)
def create_invoice_endpoint(invoice: InvoiceCreate):
    return create_invoice(invoice)

@router.get("/invoice/{id}", response_model=Invoice)
def get_invoice_endpoint(id: str):
    invoice = get_invoice(id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.get("/invoices/psychologist/{psychologist_id}", response_model=list[Invoice])
def get_invoices_by_psychologist_endpoint(psychologist_id: str):
    invoices = get_invoices_by_psychologist(psychologist_id)
    if not invoices:
        raise HTTPException(status_code=404, detail="Invoices not found")
    return invoices

@router.get("/invoices/{psychologist_id}/{patient_id}", response_model=list[Invoice])
def get_invoices_by_psychologist_patient_endpoint(psychologist_id: str, patient_id: str):
    invoices = get_invoices_by_psychologist_patient(psychologist_id, patient_id)
    if not invoices:
        raise HTTPException(status_code=404, detail="Invoices not found")
    return invoices


