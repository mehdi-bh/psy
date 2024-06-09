import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PsyDB')


def get_consultations_by_psychologist(psychologist_id: str):
    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression="GSI1_PK = :pk AND begins_with(GSI1_SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"PSYCHOLOGIST#{psychologist_id}",
            ":sk": "CONSULTATION#"
        }
    )
    items = response.get('Items', [])
    print("Query Response:", response)
    return items


# Test the function manually
if __name__ == "__main__":
    consultations = get_consultations_by_psychologist('456')
    print("Consultations:", consultations)
