
__author__ = 'Ronald T. Fernandez (Ronald Teijeira Fernandez)'
__email__ = 'ronaldtfernandez@gmail.com'
__version__ = '1.0'
__date__ = 'September 2019'

from aws_cdk import (
    aws_s3 as s3,
    aws_kms,
    core,
    aws_sns,
    aws_s3_notifications
)
import typing
from aws_cdk.core import IAspect, IConstruct
import jsii

# CDK Constructor to create a custom implementation of a Bucket.
# The behavior is similar to s3.Bucket except that buckets with numbers are forbidden.
# Additionally, we have enabled CORS rules and attached a target topic in case it is specified
class CustomS3(s3.Bucket):

  def __init__(self, scope: core.Construct, id: str, *, target_topic: aws_sns.Topic, access_control: typing.Optional["BucketAccessControl"]=None, block_public_access: typing.Optional["BlockPublicAccess"]=None, bucket_name: typing.Optional[str]=None, cors: typing.Optional[typing.List["CorsRule"]]=None, encryption: typing.Optional["BucketEncryption"]=None, encryption_key: typing.Optional[aws_kms.IKey]=None, lifecycle_rules: typing.Optional[typing.List["LifecycleRule"]]=None, metrics: typing.Optional[typing.List["BucketMetrics"]]=None, public_read_access: typing.Optional[bool]=None, removal_policy: typing.Optional[core.RemovalPolicy]=None, versioned: typing.Optional[bool]=None, website_error_document: typing.Optional[str]=None, website_index_document: typing.Optional[str]=None, website_redirect: typing.Optional["RedirectTarget"]=None, website_routing_rules: typing.Optional[typing.List["RoutingRule"]]=None) -> None:
    super().__init__(scope = scope, id = id, access_control = access_control, block_public_access=block_public_access, bucket_name=bucket_name, cors=cors, encryption=encryption, encryption_key= encryption_key, lifecycle_rules=lifecycle_rules, metrics=metrics, public_read_access=public_read_access, removal_policy=removal_policy, versioned=versioned, website_error_document=website_error_document, website_redirect=website_redirect, website_routing_rules=website_routing_rules)

    if target_topic is not None:
        dest = aws_s3_notifications.SnsDestination(target_topic)
        self.add_event_notification(s3.EventType.OBJECT_CREATED, dest)
        self.add_event_notification(s3.EventType.OBJECT_REMOVED, dest)

    self.node.apply_aspect(forbid_bucket_with_numbers(bucket_name, type(self)))

    self.add_cors_rule(allowed_methods=[s3.HttpMethods.GET], allowed_origins=['*'])


# CDK Aspect to forbid buckets with numbers
@jsii.implements(IAspect)
class forbid_bucket_with_numbers():
    def __init__(self, bucket_name, type):
        self._bucket_name = bucket_name
        self._type = type
    def visit(self, node: IConstruct) -> None:
        if self._type is s3.Bucket or self._type is CustomS3:
            has_number = any(char.isdigit() for char in self._bucket_name)
            if has_number:
                raise ValueError("Invalid Bucket Name <" +self._bucket_name + "> (it should not contain numbers)")