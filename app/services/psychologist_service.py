import boto3
from app.schemas.psychologist import PsychologistCreate

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PsyDB')

def create_psychologist(psychologist: PsychologistCreate):
    item = psychologist.model_dump()
    item['PK'] = f"PSYCHOLOGIST#{psychologist.PsychologistId}"
    item['SK'] = "METADATA"
    table.put_item(Item=item)
    return psychologist

def get_psychologist(psychologist_id: str):
    response = table.get_item(
        Key={
            'PK': f"PSYCHOLOGIST#{psychologist_id}",
            'SK': "METADATA"
        }
    )
    return response.get('Item')
