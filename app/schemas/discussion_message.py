from pydantic import BaseModel

class DiscussionMessageBase(BaseModel):
    PsychologistId: str
    PatientId: str
    Message: str
    Timestamp: str
    Sender: str
    Seen: bool

class DiscussionMessageCreate(DiscussionMessageBase):
    MessageId: str

class DiscussionMessage(DiscussionMessageBase):
    MessageId: str
