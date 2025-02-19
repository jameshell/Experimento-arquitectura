import json
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "message": "Hello from AWS Lambda via API Gateway!",
                "event": event,
            }
        )
    }
