import boto3
from decimal import Decimal
from app.schemas.invoice import InvoiceCreate

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PsyDB')

def create_invoice(invoice: InvoiceCreate):
    item = invoice.model_dump()
    item['Amount'] = Decimal(str(invoice.Amount))  # Convert float to Decimal
    item['PK'] = f"INVOICE#{invoice.InvoiceId}"
    item['SK'] = "METADATA"
    table.put_item(Item=item)
    return invoice

def get_invoice(invoice_id: str):
    response = table.get_item(
        Key={
            'PK': f"INVOICE#{invoice_id}",
            'SK': "METADATA"
        }
    )
    return response.get('Item')
