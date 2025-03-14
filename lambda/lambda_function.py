import json
import random
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configuración del porcentaje de fallo
FAILURE_RATE = 0.01  # 20% de errores
ERROR_RESPONSES = [
    (500, "Internal Server Error"),
    (503, "Service Unavailable"),
    (429, "Too Many Requests"),
]

def lambda_handler(event, context):
    # Determinar si debe fallar
    if random.random() < FAILURE_RATE:
        status_code, error_msg = random.choice(ERROR_RESPONSES)
        logger.warning(f"Simulando error {status_code}: {error_msg}")
        return {
            "statusCode": status_code,
            "body": json.dumps({"error": error_msg})
        }

    # Respuesta exitosa
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "Hello from AWS Lambda!", "event": event})
    }
