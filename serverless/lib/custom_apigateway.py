
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

# CDK Constructor to create a custom implementation of a Bucket.
# The behavior is the same as s3.Bucket except that buckets with numbers are forbidden.
class custom_apigateway(aws_apigateway.RestApi):
    def __init__(self, scope: core.Construct, id: str, *, cloud_watch_role: typing.Optional[bool]=None, deploy: typing.Optional[bool]=None, deploy_options: typing.Optional["StageOptions"]=None, description: typing.Optional[str]=None, endpoint_types: typing.Optional[typing.List["EndpointType"]]=None, fail_on_warnings: typing.Optional[bool]=None, parameters: typing.Optional[typing.Mapping[str,str]]=None, policy: typing.Optional[aws_iam.PolicyDocument]=None, rest_api_name: typing.Optional[str]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> None:
        super().__init__(scope = scope, id=id, cloud_watch_role = cloud_watch_role, deploy = deploy, deploy_options=deploy_options, description=description, endpoint_types=endpoint_types, fail_on_warnings=fail_on_warnings, parameters=parameters, policy=policy, rest_api_name=rest_api_name, default_integration=default_integration, default_method_options=default_method_options)
        
        # Define lambdas to be integrated in API
        lambda1 = aws_lambda.Function(self, 'lambda1', code = aws_lambda.InlineCode(open('serverless/lambdas/lambda1.py', encoding="utf-8").read()), handler= 'index.handler', timeout = core.Duration.seconds(30), runtime = aws_lambda.Runtime.PYTHON_3_7, environment=[])
        lambda1.add_to_role_policy(aws_iam.PolicyStatement(actions=['dynamodb:*'], effect = aws_iam.Effect.ALLOW, resources=['*']))

        lambda2 = aws_lambda.Function(self, 'lambda2', code = aws_lambda.InlineCode(open('serverless/lambdas/lambda2.py', encoding="utf-8").read()), handler= 'index.handler', timeout = core.Duration.seconds(30), runtime = aws_lambda.Runtime.PYTHON_3_7, environment=[])
        lambda2.add_to_role_policy(aws_iam.PolicyStatement(actions=['dynamodb:*'], effect = aws_iam.Effect.ALLOW, resources=['*']))

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

        # API Gateway Resource 1
        res1 = self.root.add_resource('res1')
        integration_res1 = aws_apigateway.LambdaIntegration(lambda1, proxy=False, integration_responses=integration_responses, passthrough_behavior=aws_apigateway.PassthroughBehavior.NEVER, request_templates=request_templates)
        res1.add_method('GET', integration_res1, method_responses=method_responses)
        
        # API GAteway Resource 2
        res2 = self.root.add_resource('res2')
        integration_res2 = aws_apigateway.LambdaIntegration(lambda2, proxy=False, integration_responses=integration_responses, passthrough_behavior=aws_apigateway.PassthroughBehavior.NEVER, request_templates=request_templates)
        res2.add_method('GET', integration_res2, method_responses=method_responses)

        self.node.apply_aspect(api_gateway_restrictions(type(self)))


# CDK Aspect for API Gateway Restrictions
@jsii.implements(IAspect)
class api_gateway_restrictions():
    def __init__(self, type):
        self._type = type
    def visit(self, node: IConstruct) -> None:
        if self._type is aws_apigateway.RestApi or self._type is custom_apigateway:
            return
            # TODO