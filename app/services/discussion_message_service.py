import boto3
import logging
from app.schemas.discussion_message import DiscussionMessageCreate

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PsyDB')

logger = logging.getLogger(__name__)

def create_discussion_message(message: DiscussionMessageCreate):
    item = message.model_dump()
    item['PK'] = f"DISCUSSION#{message.PsychologistId}#{message.PatientId}"
    item['SK'] = f"MESSAGE#{message.Timestamp}#{message.MessageId}"
    item['GSI1_PK'] = f"PSYCHOLOGIST#{message.PsychologistId}"
    item['GSI1_SK'] = f"DISCUSSION#{message.PatientId}#{message.Timestamp}"
    table.put_item(Item=item)
    return message


def get_discussion_messages_psychologist_patient(psychologist_id: str, patient_id: str):
    response = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"DISCUSSION#{psychologist_id}#{patient_id}",
            ":sk": "MESSAGE#"
        }
    )
    return response.get('Items')

def get_discussion_messages_by_psychologist(psychologist_id: str):
    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression="GSI1_PK = :pk AND begins_with(GSI1_SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"PSYCHOLOGIST#{psychologist_id}",
            ":sk": "DISCUSSION#"
        }
    )
    return response.get('Items', [])

