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

        # Programar una ejecución periódica con EventBridge (cada 5 minutos)
        rule = events.Rule(
            self,
            "LambdaHealthCheckRule",
            schedule=events.Schedule.rate(duration=cloudwatch.Duration.minutes(2))
        )
        rule.add_target(targets.LambdaFunction(lambda_function))

        #  MÉTRICAS PARA MONITOREO DE LA LAMBDA

        # Métrica de invocaciones exitosas
        success_metric = cloudwatch.Metric(
            namespace="AWS/Lambda",
            metric_name="Invocations",
            dimensions_map={"FunctionName": lambda_function.function_name},
            statistic="sum",
            period=cloudwatch.Duration.minutes(2)
        )

        # Métrica de errores
        error_metric = cloudwatch.Metric(
            namespace="AWS/Lambda",
            metric_name="Errors",
            dimensions_map={"FunctionName": lambda_function.function_name},
            statistic="sum",
            period=cloudwatch.Duration.minutes(2)
        )

        # Métrica de duración de ejecución
        duration_metric = cloudwatch.Metric(
            namespace="AWS/Lambda",
            metric_name="Duration",
            dimensions_map={"FunctionName": lambda_function.function_name},
            statistic="avg",
            period=cloudwatch.Duration.minutes(2)
        )

        # ALARMAS EN CLOUDWATCH

        # Alarma si la Lambda no se ejecuta en 5 minutos
        no_execution_alarm = cloudwatch.Alarm(
            self,
            "LambdaNoExecutionAlarm",
            metric=success_metric,
            threshold=1,  # Debe haber al menos 1 ejecución
            evaluation_periods=1,
            comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD
        )

        # Alarma si la Lambda empieza a fallar con errores
        error_alarm = cloudwatch.Alarm(
            self,
            "LambdaErrorAlarm",
            metric=error_metric,
            threshold=1,  # Se activará si hay al menos 1 error
            evaluation_periods=1,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD
        )

        # Alarma si la ejecución de Lambda es muy lenta
        duration_alarm = cloudwatch.Alarm(
            self,
            "LambdaSlowResponseAlarm",
            metric=duration_metric,
            threshold=3000,  # 3000 ms = 3 segundos
            evaluation_periods=1,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD
        )
