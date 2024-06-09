from pydantic import BaseModel
from typing import Optional

class Psychologist(BaseModel):
    PsychologistId: str
    FirstName: str
    LastName: str
    DateOfBirth: str
    Sex: str
    Photo: Optional[str] = None
