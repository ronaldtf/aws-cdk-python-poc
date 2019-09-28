import boto3
import os
from botocore.exceptions import (
    ClientError,
    ParamValidationError
)
import json

def handler(event, context):

    message = event.get('Records')[0].get('Sns').get('Message')
    message = json.loads(message)
    ref = message.get('Records')[0].get('s3')
    operation = message.get('Records')[0].get('eventName') # ObjectCreated:Put / ObjectRemoved:Delete
    
    bucket_name = ref.get('bucket').get('name')
    object_name = ref.get('object').get('key')

    table_name = os.environ.get('TABLENAME')

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Check the table exists
    try:
        if table.table_status == 'CREATING':
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        elif table.table_status == 'ACTIVE':
            pass
        elif table.table_status == 'DELETING':
            table.meta.client.get_waiter('table_not_exists').wait(TableName=table_name)
    except ClientError:
        # Create the table
        dynamodb.create_table(
            TableName = table_name,
            KeySchema = [
                {
                    'AttributeName': 'bucket',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'object',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions = [
                {
                    'AttributeName': 'bucket',
                    'AttributeType': 'S'
                }, {
                    'AttributeName': 'object',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        # Wait for table creation
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    
    # Read table elements to get the counter
    counter = 0
    try:
        response = table.get_item(
            Key={
                'bucket': bucket_name,
                'object': object_name
            },
            AttributesToGet = [
                'counter'
            ]
        )
        if 'Item' in response:
            counter = response['Item'].get('counter')
        else:
            counter = 0
    except ClientError as e:
        counter = 0

    print('Counter before: ' + str(int(counter)))
    counter = int(counter)
    if operation == 'ObjectCreated:Put':
        counter = counter + 1
    else:
        counter = max(0, counter - 1)
    print('Counter after: ' + str(int(counter)))

    try:
        table.update_item(
            Key={
                'bucket': bucket_name,
                'object': object_name
            }, AttributeUpdates = {
                'counter': counter
            }
        )
    except ParamValidationError:
        table.put_item(
            Item={
                'bucket': bucket_name,
                'object': object_name,
                'counter': counter
            },
        )
    