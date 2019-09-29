
__author__ = 'Ronald T. Fernandez (Ronald Teijeira Fernandez)'
__email__ = 'ronaldtfernandez@gmail.com'
__version__ = '1.0'
__date__ = 'September 2019'

import boto3
import os
from botocore.exceptions import (
    ClientError,
    ParamValidationError
)
import json

def handler(event, context):

    table_name = os.environ.get('TABLENAME')

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    try:
        response = table.scan()
        data = response['Items']

        return data
    except ClientError:
        pass