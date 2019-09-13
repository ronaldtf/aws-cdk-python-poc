__author__ = 'Ronald T. Fernandez (Ronald Teijeira Fernandez)'
__email__ = 'ronaldtfernandez@gmail.com'
__version__ = '1.0'
__date__ = 'September 2019'

from aws_cdk import core
from lib.custom_s3 import MyBucketDefinition
from lib.custom_apigateway import MyAPIGateway

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

        # Create S3 bucket
        bucket = MyBucketDefinition(self, id=bucket_name, bucket_name=bucket_name, versioned=False)
        bucket.add_cors_rule(
            allowed_origins=[],
            allowed_methods=[]
        )
        
        apigateway = MyAPIGateway(self, id=apigateway_name)
        

