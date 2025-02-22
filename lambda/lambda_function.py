import json
import time
import random
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configuración: tasa global de fallo y opciones de error
FAILURE_RATE = 0.2  # 20% de probabilidad de fallo
error_options = [
    {"statusCode": 500, "body": json.dumps({"error": "Servicio temporalmente no disponible: Internal Server Error"}), "log_level": logging.CRITICAL},
    {"statusCode": 503, "body": json.dumps({"error": "Error de autenticación: 503 Service Unavailable"}), "log_level": logging.ERROR},
    {"statusCode": 102, "body": json.dumps({"error": "Servicio temporalmente no disponible: Processing"}), "log_level": logging.INFO},
    {"statusCode": 429, "body": json.dumps({"error": "Servicio temporalmente no disponible: Too Many Requests"}), "log_level": logging.WARNING},
]

def lambda_handler(event, context):
    # Determinar si se simula un fallo
    if random.random() < FAILURE_RATE:
        error_choice = random.choice(error_options)
        logger.setLevel(error_choice["log_level"])
        print("Simulando una falla en la Lambda...")
        time.sleep(10)  # Simula latencia en la respuesta de error
        return {
            "statusCode": error_choice["statusCode"],
            "body": error_choice["body"]
        }

    # Respuesta exitosa
    return {
        'statusCode': 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "message": "Hello from AWS Lambda via API Gateway!",
            "event": event,
        })
    }
