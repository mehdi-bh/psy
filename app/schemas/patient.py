from pydantic import BaseModel
from typing import Optional, Dict

class PatientBase(BaseModel):
    FirstName: str
    LastName: str
    DateOfBirth: str
    Sex: str
    Email: str
    PhoneNumber: str
    Address: Dict[str, str]
    Description: Optional[str] = None
    Photo: Optional[str] = None

class PatientCreate(PatientBase):
    PatientId: str

class Patient(PatientBase):
    PatientId: str
