__author__ = 'Ronald T. Fernandez (Ronald Teijeira Fernandez)'
__email__ = 'ronaldtfernandez@gmail.com'
__version__ = '1.0'
__date__ = 'September 2019'

from aws_cdk import core
from lib.custom_s3 import CustomS3
from lib.custom_apigateway import CustomAPIGateway
from lib.custom_dynamodb import CustomDynamoDB
from lib.custom_sns import CustomSNS
from lib.custom_lambda_snstarget import CustomLambdaSNStarget

## This is a class to retrieve parameter values from configuration file
class Parameters:
    param_file = 'serverless/params/config.properties'

    @staticmethod
    def get_parameters():
        params = dict(line.strip().split('=') for line in open(Parameters.param_file) if not line.strip().startswith('#') and line.strip() != "")
        return params


## This is the main class used to generate the CloudFormation templates
class ServerlessStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Get parameters to build the objects
        parameters = Parameters.get_parameters()
        prefix = parameters['Prefix']
        bucket_name = prefix + parameters['BucketName']
        apigateway_name = prefix + parameters['ApiGatewayName']
        table_name = prefix + parameters['DBTableName']
        topic_name = prefix + parameters['SNSTopicName']
        lambda_snstarget_name = prefix + 'snstarget'

        # Create a DynamoDB table
        CustomDynamoDB(stack=self, table_name=table_name, partition_key='bucket', sort_key='object')
        # Create a SNS topic
        sns = CustomSNS(self, topic_name = topic_name, display_name = topic_name)
        # Create a S3 bucket and set the topic as event target
        CustomS3(self, id=bucket_name, target_topic=sns, bucket_name=bucket_name, versioned=True)
        # Create a Lambda which is triggered with the SNS topic
        CustomLambdaSNStarget(self, lambda_name = lambda_snstarget_name, source_topic = sns, table_name = table_name)
        # Create an API Gateway to get the status of the DynamoDB
        CustomAPIGateway(self, id=apigateway_name, table_name = table_name)
        
