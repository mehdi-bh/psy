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
    is_offline = os.getenv('IS_OFFLINE', 'false').lower() == 'true'

    logger.info(f"is_offline: {is_offline}")

    if is_offline:
        endpoint_url = "http://localhost:3001"
    else:
        endpoint_url = f"https://{event['requestContext']['domainName']}/{event['requestContext']['stage']}"

    logger.info(f"Endpoint URL: {endpoint_url}")

    apig_management_client = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint_url)

    # Retrieve all active connections
    connections = connections_table.scan().get('Items', [])
    logger.info(f"Active connections: {connections}")

    for conn in connections:
        logger.info(f"Sending message to connection ID: {conn['connectionId']}")
        try:
            apig_management_client.post_to_connection(
                ConnectionId=conn['connectionId'],
                Data=json.dumps(message_data)
            )
        except apig_management_client.exceptions.GoneException:
            logger.warning(f"Connection {conn['connectionId']} is gone, deleting from database.")
            connections_table.delete_item(Key={'connectionId': conn['connectionId']})
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            logger.error(f"ClientError sending message to {conn['connectionId']}: {error_code} - {error_message}")
        except EndpointConnectionError as e:
            logger.error(f"EndpointConnectionError: {str(e)}")
        except NoCredentialsError as e:
            logger.error(f"NoCredentialsError: {str(e)}")
        except PartialCredentialsError as e:
            logger.error(f"PartialCredentialsError: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error sending message to {conn['connectionId']}: {str(e)}")

    return {
        'statusCode': 200,
        'body': 'Message sent.'
    }

