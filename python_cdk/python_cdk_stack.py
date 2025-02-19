from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    # aws_sqs as sqs,
)
from constructs import Construct

class PythonCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        lambda_function = lambda_.Function(
            self,
            "ventas",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_handler",
            code=lambda_.Code.from_asset("lambda")
        )

        # Create an API Gateway and connect it to the Lambda function
        api = apigw.LambdaRestApi(
            self, "ventasAPI",
            handler=lambda_function,
            proxy=True  # Set `proxy=True` for automatic API mapping to Lambda
        )
        # example resource
        # queue = sqs.Queue(
        #     self, "PythonCdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
