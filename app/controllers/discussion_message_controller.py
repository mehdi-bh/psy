from fastapi import APIRouter, HTTPException
from app.schemas.discussion_message import DiscussionMessageCreate, DiscussionMessage
from app.services.discussion_message_service import create_discussion_message, get_discussion_message

router = APIRouter()

@router.post("/discussion_message", response_model=DiscussionMessage)
def create_discussion_message_endpoint(discussion_message: DiscussionMessageCreate):
    return create_discussion_message(discussion_message)

@router.get("/discussion_message/{psychologist_id}/{patient_id}", response_model=list[DiscussionMessage])
def get_discussion_message_endpoint(psychologist_id: str, patient_id: str):
    messages = get_discussion_message(psychologist_id, patient_id)
    if not messages:
        raise HTTPException(status_code=404, detail="Messages not found")
    return messages
