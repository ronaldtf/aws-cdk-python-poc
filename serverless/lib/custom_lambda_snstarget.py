
__author__ = 'Ronald T. Fernandez (Ronald Teijeira Fernandez)'
__email__ = 'ronaldtfernandez@gmail.com'
__version__ = '1.0'
__date__ = 'September 2019'

from aws_cdk import aws_iam
from aws_cdk import aws_sns
from aws_cdk import aws_lambda
from aws_cdk import aws_lambda_event_sources
from aws_cdk import core

class custom_lambda_snstarget(aws_lambda.Function):
    def __init__(self, scope: core.Construct, lambda_name: str, source_topic: aws_sns.Topic = None):
        
        super().__init__(scope = scope, id=lambda_name, code = aws_lambda.InlineCode(open('serverless/lambdas/lambda_snstarget.py', encoding="utf-8").read()), handler= 'index.handler', timeout = core.Duration.seconds(30), runtime = aws_lambda.Runtime.PYTHON_3_7, environment=[])

        self.Permission = aws_lambda.Permission(principal= aws_iam.ServicePrincipal('sns.amazonaws.com'), action='dynamodb:*')
        
        if source_topic is not None:
            sns_source = aws_lambda_event_sources.SnsEventSource(source_topic)
            sns_source.bind(self)