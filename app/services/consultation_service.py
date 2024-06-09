import boto3
import logging
from app.schemas.consultation import ConsultationCreate

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PsyDB')

logger = logging.getLogger(__name__)

def create_consultation(consultation: ConsultationCreate):
    item = consultation.model_dump()
    item['PK'] = f"CONSULTATION#{consultation.PsychologistId}#{consultation.PatientId}"
    item['SK'] = f"DATETIME#{consultation.DateTime}"
    item['GSI1_PK'] = f"PSYCHOLOGIST#{consultation.PsychologistId}"
    item['GSI1_SK'] = f"CONSULTATION#{consultation.PatientId}#{consultation.DateTime}"
    table.put_item(Item=item)
    return consultation


def get_consultation_by_psychologist_patient(psychologist_id: str, patient_id: str):
    response = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"CONSULTATION#{psychologist_id}#{patient_id}",
            ":sk": "DATETIME#"
        }
    )
    return response.get('Items')

def get_consultations_by_psychologist(psychologist_id: str):
    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression="GSI1_PK = :pk AND begins_with(GSI1_SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"PSYCHOLOGIST#{psychologist_id}",
            ":sk": "CONSULTATION#"
        }
    )
    return response.get('Items', [])
