from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    aws_cloudwatch as cloudwatch,
    aws_logs as logs,
    aws_events as events,
    aws_events_targets as targets,
    aws_cognito as cognito,
    CfnOutput
    # aws_sqs as sqs,
)
from constructs import Construct

class PythonCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #Create a Cognito User Pool
        user_pool = cognito.UserPool(
            self,
            "TestUserPool",
            user_pool_name="test-user-pool",
            self_sign_up_enabled=False,  # Disable self-signup
            sign_in_aliases=cognito.SignInAliases(
                email=True,  # Allow sign-in with email
            ),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(
                    required=True,
                    mutable=True,
                ),
            ),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=True,
            ),
        )

        # Create a User Pool Client
        user_pool_client = cognito.UserPoolClient(
            self,
            "TestUserPoolClient",
            user_pool=user_pool,
            generate_secret=False,  # Set to True if you need a client secret
        )

        # Create Admin Group
        admin_group = cognito.CfnUserPoolGroup(
            self,
            "AdminGroup",
            user_pool_id=user_pool.user_pool_id,
            group_name="Admins",
            description="Administrator group",
        )

        # Create Users Group
        users_group = cognito.CfnUserPoolGroup(
            self,
            "UsersGroup",
            user_pool_id=user_pool.user_pool_id,
            group_name="Users",
            description="Regular users group",
        )

        # Output important values
        CfnOutput(
            self,
            "UserPoolId",
            value=user_pool.user_pool_id,
        )

        CfnOutput(
            self,
            "UserPoolClientId",
            value=user_pool_client.user_pool_client_id,
        )

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
            threshold=3000,  # 3 seconds
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


        cognito_authorizer = apigw.CognitoUserPoolsAuthorizer(
            self,
            "CognitoAuthorizer",
            cognito_user_pools=[user_pool]
        )

        # Create an API Gateway and connect it to the Lambda function with the Cognito Authorizer
        api = apigw.LambdaRestApi(
            self,
            "ventasAPI",
            handler=lambda_function,
            proxy=True,
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
                allow_headers=['Content-Type', 'Authorization']
            ),
            default_method_options=apigw.MethodOptions(
                authorization_type=apigw.AuthorizationType.COGNITO,
                authorizer=cognito_authorizer
            )
        )




