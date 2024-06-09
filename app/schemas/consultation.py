from pydantic import BaseModel
from typing import Optional

class ConsultationBase(BaseModel):
    PsychologistId: str
    PatientId: str
    DateTime: str
    GoogleMeetLink: Optional[str] = None
    Status: str
    InvoiceId: str

class ConsultationCreate(ConsultationBase):
    ConsultationId: str

class Consultation(ConsultationBase):
    ConsultationId: str
