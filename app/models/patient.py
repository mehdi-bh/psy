from pydantic import BaseModel
from typing import Optional, Dict

class Patient(BaseModel):
    PatientId: str
    FirstName: str
    LastName: str
    DateOfBirth: str
    Sex: str
    Email: str
    PhoneNumber: str
    Address: Dict[str, str]
    Description: Optional[str] = None
    Photo: Optional[str] = None
