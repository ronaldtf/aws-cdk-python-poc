__author__ = 'Ronald T. Fernandez (Ronald Teijeira Fernandez)'
__email__ = 'ronaldtfernandez@gmail.com'
__version__ = '1.0'
__date__ = 'September 2019'

from aws_cdk import core
from lib.custom_s3 import custom_s3
from lib.custom_apigateway import custom_apigateway
from lib.custom_dynamodb import custom_dynamodb
from lib.custom_sns import custom_sns
from lib.custom_lambda_snstarget import custom_lambda_snstarget

## This is a class to retrieve parameter values from configuration file
class Parameters:
    param_file = 'serverless/params/config.properties'

    @staticmethod
    def get_parameters():
        params = dict(line.strip().split('=') for line in open(Parameters.param_file) if not line.strip().startswith('#') and line.strip() != "")
        return params


## This is the main class when generating the CloudFormation templates
class ServerlessStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Get parameters
        parameters = Parameters.get_parameters()
        prefix = parameters['Prefix']
        bucket_name = prefix + parameters['BucketName']
        apigateway_name = prefix + parameters['ApiGatewayName']
        table_name = prefix + parameters['DBTableName']
        partition_key = prefix + parameters['DBTablePartitionKey']
        sort_key = None if parameters['DBTableSortKey'] == '' else prefix + parameters['DBTableSortKey']
        topic_name = prefix + parameters['SNSTopicName']
        lambda_snstarget_name = prefix + 'snstarget'

        # Create S3 bucket
        sns = custom_sns(self, topic_name = topic_name, display_name = topic_name)
        dbtable = custom_dynamodb(stack=self, table_name=table_name, partition_key=partition_key, sort_key=sort_key)
        lambda_snstarget = custom_lambda_snstarget(self, lambda_name = lambda_snstarget_name, source_topic = sns, table_name = table_name)
        bucket = custom_s3(self, id=bucket_name, target_topic=sns, bucket_name=bucket_name, versioned=True)
        apigateway = custom_apigateway(self, id=apigateway_name, table_name = table_name)
        
