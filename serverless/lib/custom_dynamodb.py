
__author__ = 'Ronald T. Fernandez (Ronald Teijeira Fernandez)'
__email__ = 'ronaldtfernandez@gmail.com'
__version__ = '1.0'
__date__ = 'September 2019'

from aws_cdk import aws_dynamodb
from aws_cdk import aws_iam
from aws_cdk import core
import typing

import typing

# This class does not inherit from the CDK library DynamoDB. 
# Instead, it calls the constructor with the right parameters
class CustomDynamoDB:
    def __init__(self, stack: core.Stack, table_name: str, partition_key: str, sort_key=None):
        items_table = aws_dynamodb.Table(
            stack, 
            id=table_name,
            table_name=table_name,
            partition_key=aws_dynamodb.Attribute(
                name=partition_key,
                type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name=sort_key,
                type=aws_dynamodb.AttributeType.STRING
            ),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            stream=aws_dynamodb.StreamViewType.NEW_IMAGE,

            # The default removal policy is RETAIN, which means that cdk
            # destroy will not attempt to delete the new table, and it will
            # remain in your account until manually deleted. By setting the
            # policy to DESTROY, cdk destroy will delete the table (even if it
            # has data in it)
            removal_policy=core.RemovalPolicy.DESTROY # NOT recommended for production code
        )