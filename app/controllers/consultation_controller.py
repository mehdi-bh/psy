from fastapi import APIRouter, HTTPException
from app.schemas.consultation import ConsultationCreate, Consultation
from app.services.consultation_service import create_consultation, get_consultation

router = APIRouter()

@router.post("/consultation", response_model=Consultation)
def create_consultation_endpoint(consultation: ConsultationCreate):
    return create_consultation(consultation)

@router.get("/consultation/{psychologist_id}/{patient_id}", response_model=list[Consultation])
def get_consultation_endpoint(psychologist_id: str, patient_id: str):
    consultations = get_consultation(psychologist_id, patient_id)
    if not consultations:
        raise HTTPException(status_code=404, detail="Consultations not found")
    return consultations
