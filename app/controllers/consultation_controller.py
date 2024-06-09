import logging
from fastapi import APIRouter, HTTPException
from app.schemas.consultation import ConsultationCreate, Consultation
from app.services.consultation_service import (create_consultation, get_consultation_by_psychologist_patient,
                                               get_consultations_by_psychologist)

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/consultation", response_model=Consultation)
def create_consultation_endpoint(consultation: ConsultationCreate):
    return create_consultation(consultation)

@router.get("/consultations/psychologist/{psychologist_id}", response_model=list[Consultation])
def get_consultations_by_psychologist_endpoint(psychologist_id: str):
    consultations = get_consultations_by_psychologist(psychologist_id)
    if not consultations:
        raise HTTPException(status_code=404, detail="Consultations not found")
    return consultations

@router.get("/consultations/{psychologist_id}/{patient_id}", response_model=list[Consultation])
def get_consultations_by_psychologist_patient_endpoint(psychologist_id: str, patient_id: str):
    consultations = get_consultation_by_psychologist_patient(psychologist_id, patient_id)
    if not consultations:
        raise HTTPException(status_code=404, detail="Consultations not found")
    return consultations


