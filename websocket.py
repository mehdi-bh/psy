import json
import os
import boto3
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
connections_table = dynamodb.Table('WebSocketConnections')
psy_db_table = dynamodb.Table('PsyDB')


def connect(event, context):
    connection_id = event['requestContext']['connectionId']
    connections_table.put_item(Item={'connectionId': connection_id})
    return {
        'statusCode': 200,
        'body': 'Connected.'
    }


def disconnect(event, context):
    connection_id = event['requestContext']['connectionId']
    connections_table.delete_item(Key={'connectionId': connection_id})
    return {
        'statusCode': 200,
        'body': 'Disconnected.'
    }


def default(event, context):
    return {
        'statusCode': 200,
        'body': 'Default message.'
    }


def send_message(event, context):
    logger.info("Entering send_message function")
    connection_id = event['requestContext']['connectionId']
    body = json.loads(event['body'])
    message_data = body['data']

    logger.info(f"Received message data: {message_data}")

    # Store the message in DynamoDB (similar to create_discussion_message)
    item = {
        'PK': f"DISCUSSION#{message_data['PsychologistId']}#{message_data['PatientId']}",
        'SK': f"MESSAGE#{message_data['Timestamp']}#{message_data['MessageId']}",
        'GSI1_PK': f"PSYCHOLOGIST#{message_data['PsychologistId']}",
        'GSI1_SK': f"DISCUSSION#{message_data['PatientId']}#{message_data['Timestamp']}",
        **message_data
    }
    psy_db_table.put_item(Item=item)

    logger.info(f"Stored item in DynamoDB: {item}")

    # Determine if running in local environment
    is_offline = os.getenv('IS_OFFLINE')

    if is_offline:
        endpoint_url = "http://localhost:3001"
    else:
        endpoint_url = f"https://{event['requestContext']['domainName']}/{event['requestContext']['stage']}"

    apig_management_client = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint_url)

    # Retrieve all active connections
    connections = connections_table.scan().get('Items', [])
    for conn in connections:
        logger.info(f"Sending message to connection ID: {conn['connectionId']}")
        try:
            apig_management_client.post_to_connection(
                ConnectionId=conn['connectionId'],
                Data=json.dumps(message_data)
            )
        except Exception as e:
            logger.error(f"Error sending message to {conn['connectionId']}: {str(e)}")

    return {
        'statusCode': 200,
        'body': 'Message sent.'
    }
