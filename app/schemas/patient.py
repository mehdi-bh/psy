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
    PsychologistId: str

class PatientCreate(PatientBase):
    PatientId: str

class Patient(PatientBase):
    PatientId: str

class PatientUpdate(BaseModel):
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    DateOfBirth: Optional[str] = None
    Sex: Optional[str] = None
    Email: Optional[str] = None
    PhoneNumber: Optional[str] = None
    Address: Optional[Dict[str, str]] = None
    Description: Optional[str] = None
    Photo: Optional[str] = None
    PsychologistId: Optional[str] = None
