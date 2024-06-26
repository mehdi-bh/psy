import json
import boto3
import logging

from app.websocket.helper import store_message, post_to_connection, get_endpoint_url, get_connections

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
connections_table = dynamodb.Table('WebSocketConnections')
psy_db_table = dynamodb.Table('PsyDB')

def connect(event, context):
    connection_id = event['requestContext']['connectionId']
    user_id = event['queryStringParameters']['userId']
    user_type = event['queryStringParameters']['userType']

    pk = f"{user_type}#{user_id}"
    connections_table.put_item(Item={'PK': pk, 'connectionId': connection_id})

    return {
        'statusCode': 200,
        'body': 'Connected.'
    }

def disconnect(event, context):
    connection_id = event['requestContext']['connectionId']
    response = connections_table.scan(
        FilterExpression='connectionId = :connectionId',
        ExpressionAttributeValues={':connectionId': connection_id}
    )
    items = response.get('Items', [])
    for item in items:
        connections_table.delete_item(Key={'PK': item['PK'], 'connectionId': item['connectionId']})

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
    body = json.loads(event['body'])
    message_data = body['data']

    store_message(message_data)

    endpoint_url = get_endpoint_url(event)
    apig_management_client = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint_url)

    psychologist_connections = get_connections(f"PSYCHOLOGIST#{message_data['PsychologistId']}")
    patient_connections = get_connections(f"PATIENT#{message_data['PatientId']}")

    connections = psychologist_connections + patient_connections

    for conn in connections:
        post_to_connection(apig_management_client, conn['connectionId'], message_data)

    return {
        'statusCode': 200,
        'body': 'Message sent.'
    }
