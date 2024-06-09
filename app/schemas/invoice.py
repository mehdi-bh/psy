from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class InvoiceBase(BaseModel):
    ConsultationId: str
    PsychologistId: str
    PatientId: str
    Status: str
    Amount: Decimal
    PaymentLink: Optional[str] = None
    PDF: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    InvoiceId: str

class Invoice(InvoiceBase):
    InvoiceId: str
