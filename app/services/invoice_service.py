import boto3
import logging
from decimal import Decimal
from app.schemas.invoice import InvoiceCreate

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PsyDB')

logger = logging.getLogger(__name__)

def create_invoice(invoice: InvoiceCreate):
    item = invoice.model_dump()
    item['Amount'] = Decimal(str(invoice.Amount))  # Convert float to Decimal
    item['PK'] = f"INVOICE#{invoice.InvoiceId}"
    item['SK'] = "METADATA"
    item['GSI1_PK'] = f"PSYCHOLOGIST#{invoice.PsychologistId}"
    item['GSI1_SK'] = f"INVOICE#{invoice.PatientId}#{invoice.InvoiceId}#"
    table.put_item(Item=item)
    return invoice


def get_invoice(invoice_id: str):
    response = table.get_item(
        Key={
            'PK': f"INVOICE#{invoice_id}",
            'SK': "METADATA"
        }
    )
    logger.info("fdp")
    return response.get('Item')

def get_invoices_by_psychologist(psychologist_id: str):
    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression="GSI1_PK = :pk AND begins_with(GSI1_SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"PSYCHOLOGIST#{psychologist_id}",
            ":sk": "INVOICE#"
        }
    )
    return response.get('Items', [])

def get_invoices_by_psychologist_patient(psychologist_id: str, patient_id: str):
    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression="GSI1_PK = :pk AND begins_with(GSI1_SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"PSYCHOLOGIST#{psychologist_id}",
            ":sk": f"INVOICE#{patient_id}"
        }
    )
    return response.get('Items', [])
