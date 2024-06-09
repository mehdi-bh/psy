import boto3
from app.schemas.discussion_message import DiscussionMessageCreate

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PsyDB')

def create_discussion_message(message: DiscussionMessageCreate):
    item = message.model_dump()
    item['PK'] = f"DISCUSSION#{message.PsychologistId}#{message.PatientId}"
    item['SK'] = f"MESSAGE#{message.Timestamp}#{message.MessageId}"
    table.put_item(Item=item)
    return message

def get_discussion_message(psychologist_id: str, patient_id: str):
    response = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"DISCUSSION#{psychologist_id}#{patient_id}",
            ":sk": "MESSAGE#"
        }
    )
    return response.get('Items')
