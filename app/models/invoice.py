from pydantic import BaseModel
from typing import Optional

class Invoice(BaseModel):
    InvoiceId: str
    Status: str
    Amount: float
    PaymentLink: Optional[str] = None
    PDF: Optional[str] = None
