from pydantic import BaseModel
from typing import Optional

class Consultation(BaseModel):
    ConsultationId: str
    PsychologistId: str
    PatientId: str
    InvoiceId: str
    DateTime: str
    GoogleMeetLink: Optional[str] = None
    Status: str
