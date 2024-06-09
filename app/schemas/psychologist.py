from pydantic import BaseModel
from typing import Optional

class PsychologistBase(BaseModel):
    FirstName: str
    LastName: str
    DateOfBirth: str
    Sex: str
    Photo: Optional[str] = None

class PsychologistCreate(PsychologistBase):
    PsychologistId: str

class Psychologist(PsychologistBase):
    PsychologistId: str
