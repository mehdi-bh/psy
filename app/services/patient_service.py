import boto3
from app.schemas.patient import PatientCreate, PatientUpdate

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PsyDB')

def create_patient(patient: PatientCreate):
    item = patient.model_dump()
    item['PK'] = f"PATIENT#{patient.PatientId}"
    item['SK'] = "METADATA"
    item['GSI1_PK'] = f"PSYCHOLOGIST#{patient.PsychologistId}"
    item['GSI1_SK'] = f"PATIENT#{patient.PatientId}"
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

def get_patients_by_psychologist(psychologist_id: str):
    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression="GSI1_PK = :pk AND begins_with(GSI1_SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"PSYCHOLOGIST#{psychologist_id}",
            ":sk": "PATIENT#"
        }
    )
    return response.get('Items', [])

def update_patient(patient_id: str, patient_update: PatientUpdate):
    patient = get_patient(patient_id)
    if not patient:
        return None

    updated_fields = patient_update.model_dump(exclude_unset=True)
    for key, value in updated_fields.items():
        patient[key] = value

    table.put_item(Item=patient)
    return patient
