import jsii
from aws_cdk import core
from lib.custom_s3 import MyBucketDefinition

def getProperties():

    properties = dict(line.strip().split('=') for line in open('serverless/config/config.properties') if not line.strip().startswith('#'))
    return properties
        

class ServerlessStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        properties = getProperties()
        bucket_name = properties['BucketName']
        bucket = MyBucketDefinition(self, id=bucket_name, bucket_name=bucket_name, versioned=False)
        bucket.add_cors_rule(
            allowed_origins=['*'],
            allowed_methods=[]
        )

