
__author__ = 'Ronald T. Fernandez (Ronald Teijeira Fernandez)'
__email__ = 'ronaldtfernandez@gmail.com'
__version__ = '1.0'
__date__ = 'September 2019'

from aws_cdk import aws_sns
from aws_cdk import core
from aws_cdk import aws_iam

import typing

class custom_sns(aws_sns.Topic):
    def __init__(self, scope: core.Construct, display_name: str, topic_name: str):
        super().__init__(scope=scope, id=topic_name, display_name = display_name, topic_name = topic_name)

        policy_statement = aws_iam.PolicyStatement(actions=['SNS:Subscribe', 'SNS:publish'], conditions=[], effect=aws_iam.Effect.ALLOW, resources=[self.topic_arn], principals=[aws_iam.ArnPrincipal('*')])
        
        self.add_to_resource_policy(policy_statement)

