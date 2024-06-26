import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PsyDB')

# Sample data for each entity
patient = {
    'PK': 'PATIENT#123',
    'SK': 'METADATA',
    'PatientId': '123',
    'PsychologistId': '456',
    'FirstName': 'John',
    'LastName': 'Doe',
    'DateOfBirth': '1990-01-01',
    'Sex': 'Male',
    'Email': 'john.doe@example.com',
    'PhoneNumber': '1234567890',
    'Address': {
        'street': '123 Main St',
        'number': '1',
        'postal_code': '12345',
        'city': 'Any town',
        'country': 'Country'
    },
    'Description': 'A test patient',
    'Photo': 'https://example.com/photo.jpg',
    'GSI1_PK': 'PSYCHOLOGIST#456',
    'GSI1_SK': 'PATIENT#123'
}

psychologist = {
    'PK': 'PSYCHOLOGIST#456',
    'SK': 'METADATA',
    'PsychologistId': '456',
    'FirstName': 'Jane',
    'LastName': 'Smith',
    'DateOfBirth': '1980-02-02',
    'Sex': 'Female',
    'Photo': 'https://example.com/photo.jpg'
}

discussion_message = {
    'PK': 'DISCUSSION#456#123',
    'SK': 'MESSAGE#2023-01-01T12:00:00Z#789',
    'MessageId': '789',
    'PsychologistId': '456',
    'PatientId': '123',
    'Message': 'Hello, how are you?',
    'Timestamp': '2023-01-01T12:00:00Z',
    'Sender': 'Patient',
    'Seen': False,
    'GSI1_PK': 'PSYCHOLOGIST#456',
    'GSI1_SK': 'DISCUSSION#123#2023-01-01T12:00:00Z'
}

discussion_message_2 = {
    'PK': 'DISCUSSION#456#123',
    'SK': 'MESSAGE#2023-01-01T12:10:10Z#790',
    'MessageId': '790',
    'PsychologistId': '456',
    'PatientId': '123',
    'Message': 'Hello, how are you?',
    'Timestamp': '2023-01-01T12:10:10Z',
    'Sender': 'Patient',
    'Seen': False,
    'GSI1_PK': 'PSYCHOLOGIST#456',
    'GSI1_SK': 'DISCUSSION#123#2023-01-01T12:10:10Z'
}

consultation = {
    'PK': 'CONSULTATION#456#123',
    'SK': 'DATETIME#2023-01-15T10:00:00Z',
    'ConsultationId': '101112',
    'PsychologistId': '456',
    'PatientId': '123',
    'DateTime': '2023-01-15T10:00:00Z',
    'GoogleMeetLink': 'https://meet.google.com/example',
    'Status': 'Scheduled',
    'InvoiceId': '151617',
    'GSI1_PK': 'PSYCHOLOGIST#456',
    'GSI1_SK': 'CONSULTATION#123#2023-01-15T10:00:00Z'
}

invoice = {
    'PK': 'INVOICE#151617',
    'SK': 'METADATA',
    'InvoiceId': '151617',
    'PatientId': '123',
    'PsychologistId': '456',
    'ConsultationId': '101112',
    'Status': 'Not Paid',
    'Amount': Decimal('100.0'),
    'PaymentLink': 'https://payment.example.com',
    'PDF': 'https://example.com/invoice.pdf',
    'GSI1_PK': 'PSYCHOLOGIST#456',
    'GSI1_SK': 'INVOICE#123#151617'
}

# List of all items to put in the database
items = [patient, psychologist, discussion_message, discussion_message_2, consultation, invoice]

# Putting items in the database
for item in items:
    table.put_item(Item=item)

print("Database populated with sample data.")


