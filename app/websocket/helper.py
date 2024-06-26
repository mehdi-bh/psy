import json
import os
import boto3
import logging
from botocore.exceptions import ClientError, EndpointConnectionError, NoCredentialsError, PartialCredentialsError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
connections_table = dynamodb.Table('WebSocketConnections')
psy_db_table = dynamodb.Table('PsyDB')

def get_endpoint_url(event):
    is_offline = os.getenv('IS_OFFLINE', 'false').lower() == 'true'
    return "http://localhost:3001" if is_offline else f"https://{event['requestContext']['domainName']}/{event['requestContext']['stage']}"

def get_connections(pk):
    response = connections_table.query(
        KeyConditionExpression='PK = :pk',
        ExpressionAttributeValues={':pk': pk}
    )
    return response.get('Items', [])

def store_message(message_data):
    item = {
        'PK': f"DISCUSSION#{message_data['PsychologistId']}#{message_data['PatientId']}",
        'SK': f"MESSAGE#{message_data['Timestamp']}#{message_data['MessageId']}",
        'GSI1_PK': f"PSYCHOLOGIST#{message_data['PsychologistId']}",
        'GSI1_SK': f"DISCUSSION#{message_data['PatientId']}#{message_data['Timestamp']}",
        **message_data
    }
    psy_db_table.put_item(Item=item)

def post_to_connection(apig_management_client, connection_id, message_data):
    try:
        apig_management_client.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps(message_data)
        )
    except apig_management_client.exceptions.GoneException:
        logger.warning(f"Connection {connection_id} is gone, deleting from database.")
        connections_table.delete_item(Key={'PK': connection_id, 'connectionId': connection_id})
    except ClientError as e:
        logger.error(f"ClientError: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
    except (EndpointConnectionError, NoCredentialsError, PartialCredentialsError) as e:
        logger.error(f"{type(e).__name__}: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")