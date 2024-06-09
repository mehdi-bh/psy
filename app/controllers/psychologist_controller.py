from fastapi import APIRouter, HTTPException
from app.schemas.psychologist import PsychologistCreate, Psychologist
from app.services.psychologist_service import create_psychologist, get_psychologist

router = APIRouter()

@router.post("/psychologist", response_model=Psychologist)
def create_psychologist_endpoint(psychologist: PsychologistCreate):
    return create_psychologist(psychologist)

@router.get("/psychologist/{id}", response_model=Psychologist)
def get_psychologist_endpoint(id: str):
    psychologist = get_psychologist(id)
    if psychologist is None:
        raise HTTPException(status_code=404, detail="Psychologist not found")
    return psychologist
