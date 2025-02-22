from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    aws_cloudwatch as cloudwatch,
    aws_logs as logs,
    aws_events as events,
    aws_events_targets as targets
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

        # Create Cloudwatch alarms for the Lambda function
        # 1. Error Rate Alarm: Triggers when any errors occur in your Lambda function
        errors_alarm = cloudwatch.Alarm(
            self,
            "LambdaErrorsAlarm",
            metric=lambda_function.metric_errors(),
            threshold=1,
            evaluation_periods=1,
            alarm_description="Alarm if the Lambda function has any errors",
            alarm_name="LambdaFunctionErrors",
        )

        # 2. Invocation Duration Alarm: Monitors execution time and alerts if it exceeds 5 seconds
        duration_alarm = cloudwatch.Alarm(
            self,
            "LambdaDurationAlarm",
            metric=lambda_function.metric_duration(),
            threshold=5000,  # 5 seconds
            evaluation_periods=1,
            alarm_description="Alarm if the Lambda function duration exceeds 5 seconds",
            alarm_name="LambdaFunctionDuration",
        )

        # 3. Throttles Alarm: Alerts when your function is being throttled
        throttles_alarm = cloudwatch.Alarm(
            self,
            "LambdaThrottlesAlarm",
            metric=lambda_function.metric_throttles(),
            threshold=1,
            evaluation_periods=1,
            alarm_description="Alarm if the Lambda function is being throttled",
            alarm_name="LambdaFunctionThrottles",
        )

        # 4. Invocations Alarm (for monitoring activity)
        invocations_alarm = cloudwatch.Alarm(
            self,
            "LambdaInvocationsAlarm",
            metric=lambda_function.metric_invocations(),
            threshold=1,
            evaluation_periods=5,
            comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
            alarm_description="Alarm if the Lambda function has low/no invocations",
            alarm_name="LambdaFunctionInvocations",
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



