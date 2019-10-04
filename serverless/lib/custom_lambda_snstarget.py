
__author__ = 'Ronald T. Fernandez (Ronald Teijeira Fernandez)'
__email__ = 'ronaldtfernandez@gmail.com'
__version__ = '1.0'
__date__ = 'September 2019'

from aws_cdk import aws_iam
from aws_cdk import aws_sns
from aws_cdk import aws_lambda
from aws_cdk import aws_lambda_event_sources
from aws_cdk import core

# Lambda function that works as a target to a SNS topic with a specific purpose (access to DynamoDB to update it)
# The behavior of the lambda is implemented in 'serverless/lambdas/lambda_snstarget.py' file
class CustomLambdaSNStarget(aws_lambda.Function):
    def __init__(self, scope: core.Construct, lambda_name: str, source_topic: aws_sns.Topic = None, table_name : str = 'S3Table'):
        
        super().__init__(scope = scope, id=lambda_name, code = aws_lambda.InlineCode(open('serverless/lambdas/lambda_snstarget.py', encoding="utf-8").read()), handler= 'index.handler', timeout = core.Duration.seconds(30), runtime = aws_lambda.Runtime.PYTHON_3_7, environment = {'TABLENAME':table_name})
        self.add_to_role_policy(aws_iam.PolicyStatement(actions=['dynamodb:*'], effect = aws_iam.Effect.ALLOW, resources = ['*']))
        if source_topic is not None:
            sns_source = aws_lambda_event_sources.SnsEventSource(source_topic)
            sns_source.bind(self)