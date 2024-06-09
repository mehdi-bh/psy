from fastapi import APIRouter, HTTPException
from app.schemas.patient import PatientCreate, Patient
from app.services.patient_service import create_patient, get_patient

router = APIRouter()

@router.post("/patient", response_model=Patient)
def create_patient_endpoint(patient: PatientCreate):
    return create_patient(patient)

@router.get("/patient/{id}", response_model=Patient)
def get_patient_endpoint(id: str):
    patient = get_patient(id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
