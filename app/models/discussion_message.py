from pydantic import BaseModel

class DiscussionMessage(BaseModel):
    MessageId: str
    PsychologistId: str
    PatientId: str
    Message: str
    Timestamp: str
    Sender: str
    Seen: bool
