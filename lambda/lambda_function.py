import json
import time
import random
import logging

logger = logging.getLogger()

def lambda_handler(event, context):
    if random.random() < 0.2:
        print("Simulando una falla en la Lambda...")
        logger.setLevel(logging.CRITICAL)
        time.sleep(10)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Servicio temporalmente no disponible: Internal Server Error"})
        }

    if random.random() < 0.2:
        print("Simulando una falla en la Lambda...")
        logger.setLevel(logging.ERROR)
        time.sleep(10)
        return {
            "statusCode": 503,
            "body": json.dumps({"error": "Error de autenticación: 503 Service Unavailable"})
        }

    if random.random() < 0.2:
        print("Simulando una falla en la Lambda...")
        logger.setLevel(logging.INFO)
        time.sleep(10)
        return {
            "statusCode": 102,
            "body": json.dumps({"error": "Servicio temporalmente no disponible:Processing"})
        }

    if random.random() < 0.2:
        print("Simulando una falla en la Lambda...")
        logger.setLevel(logging.WARNING)
        time.sleep(10)
        return {
            "statusCode": 429,
            "body": json.dumps({"error": "Servicio temporalmente no disponible: Too Many Requests"})
        }

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
