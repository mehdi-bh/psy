import boto3
from app.schemas.patient import PatientCreate

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PsyDB')

def create_patient(patient: PatientCreate):
    item = patient.model_dump()
    item['PK'] = f"PATIENT#{patient.PatientId}"
    item['SK'] = "METADATA"
    table.put_item(Item=item)
    return patient

def get_patient(patient_id: str):
    response = table.get_item(
        Key={
            'PK': f"PATIENT#{patient_id}",
            'SK': "METADATA"
        }
    )
    return response.get('Item')
