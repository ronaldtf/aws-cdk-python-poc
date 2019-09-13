__author__ = 'Ronald T. Fernandez (Ronald Teijeira Fernandez)'
__email__ = 'ronaldtfernandez@gmail.com'
__version__ = '1.0'
__date__ = 'September 2019'

import jsii
from aws_cdk import core
from lib.custom_s3 import MyBucketDefinition

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

        
        parameters = Parameters.get_parameters()
        bucket_name = parameters['BucketName']
        bucket = MyBucketDefinition(self, id=bucket_name, bucket_name=bucket_name, versioned=False)
        bucket.add_cors_rule(
            allowed_origins=['*'],
            allowed_methods=[]
        )

