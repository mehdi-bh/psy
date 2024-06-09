import boto3
from app.schemas.consultation import ConsultationCreate

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PsyDB')

def create_consultation(consultation: ConsultationCreate):
    item = consultation.model_dump()
    item['PK'] = f"CONSULTATION#{consultation.PsychologistId}#{consultation.PatientId}"
    item['SK'] = f"DATETIME#{consultation.DateTime}"
    table.put_item(Item=item)
    return consultation

def get_consultation(psychologist_id: str, patient_id: str):
    response = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"CONSULTATION#{psychologist_id}#{patient_id}",
            ":sk": "DATETIME#"
        }
    )
    return response.get('Items')
