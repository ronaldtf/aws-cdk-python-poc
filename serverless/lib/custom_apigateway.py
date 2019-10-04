
__author__ = 'Ronald T. Fernandez (Ronald Teijeira Fernandez)'
__email__ = 'ronaldtfernandez@gmail.com'
__version__ = '1.0'
__date__ = 'September 2019'

from aws_cdk import (
    aws_apigateway,
    aws_lambda,
    aws_iam,
    core
)
import typing
from aws_cdk.core import IAspect, IConstruct
import jsii

# Defines an API Gateway with a specific resource to get the information from a DynamoDB database.
# The lambda code is in 'serverless/lambdas/lambda_get_count.py'
class CustomAPIGateway(aws_apigateway.RestApi):
    def __init__(self, scope: core.Construct, id: str, *, cloud_watch_role: typing.Optional[bool]=None, deploy: typing.Optional[bool]=None, deploy_options: typing.Optional["StageOptions"]=None, description: typing.Optional[str]=None, endpoint_types: typing.Optional[typing.List["EndpointType"]]=None, fail_on_warnings: typing.Optional[bool]=None, parameters: typing.Optional[typing.Mapping[str,str]]=None, policy: typing.Optional[aws_iam.PolicyDocument]=None, rest_api_name: typing.Optional[str]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None, table_name: str) -> None:
        super().__init__(scope = scope, id=id, cloud_watch_role = cloud_watch_role, deploy = deploy, deploy_options=deploy_options, description=description, endpoint_types=endpoint_types, fail_on_warnings=fail_on_warnings, parameters=parameters, policy=policy, rest_api_name=rest_api_name, default_integration=default_integration, default_method_options=default_method_options)
        
        # Define lambdas to be integrated in API
        lambda_get_count = aws_lambda.Function(self, 'lambda_get_count', code = aws_lambda.InlineCode(open('serverless/lambdas/lambda_get_count.py', encoding="utf-8").read()), handler= 'index.handler', timeout = core.Duration.seconds(30), runtime = aws_lambda.Runtime.PYTHON_3_7, environment = {'TABLENAME':table_name})
        lambda_get_count.add_to_role_policy(aws_iam.PolicyStatement(actions=['dynamodb:*'], effect = aws_iam.Effect.ALLOW, resources=['*']))

        # Common API Gateway options
        integration_responses = [
            {
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent'",
                    'method.response.header.Access-Control-Allow-Origin': "'*'",
                    'method.response.header.Access-Control-Allow-Credentials': "'false'",
                    'method.response.header.Access-Control-Allow-Methods': "'OPTIONS,GET,PUT,POST,DELETE'",
                }
            }
        ]
        method_responses=[{
            'statusCode': '200',
            'responseParameters': {
                'method.response.header.Access-Control-Allow-Headers': True,
                'method.response.header.Access-Control-Allow-Methods': True,
                'method.response.header.Access-Control-Allow-Credentials': True,
                'method.response.header.Access-Control-Allow-Origin': True,
            },  
        }]
        request_templates={
            "application/json": "{\"statusCode\": 200}"
        }

        # API Gateway Resource
        get_count = self.root.add_resource('count')
        integration_get_count = aws_apigateway.LambdaIntegration(lambda_get_count, proxy=False, integration_responses=integration_responses, passthrough_behavior=aws_apigateway.PassthroughBehavior.NEVER, request_templates=request_templates)
        get_count.add_method('GET', integration_get_count, method_responses=method_responses)
        