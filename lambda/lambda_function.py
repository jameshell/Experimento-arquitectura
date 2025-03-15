import json
import os
import jwt
import requests
from jwt.algorithms import RSAAlgorithm

# Obtener la URL de las claves públicas de Cognito
JWKS_URL = f"https://cognito-idp.{os.environ['REGION']}.amazonaws.com/{os.environ['USER_POOL_ID']}/.well-known/jwks.json"


def get_signing_key(kid):

    try:
        response = requests.get(JWKS_URL)
        jwks = response.json()
        for key in jwks['keys']:
            if key['kid'] == kid:
                return RSAAlgorithm.from_jwk(json.dumps(key))
    except Exception as e:
        print("Error obteniendo JWKS:", e)
    return None


def lambda_handler(event, context):

    token = event.get("headers", {}).get("Authorization", "").replace("Bearer ", "")

    if not token:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Token no proporcionado"})
        }

    try:
        # Decodificar sin verificar para extraer el 'kid'
        unverified_header = jwt.get_unverified_header(token)
        signing_key = get_signing_key(unverified_header["kid"])

        if not signing_key:
            return {
                "statusCode": 401,
                "body": json.dumps({"message": "Clave de firma no encontrada"})
            }

        # Verificar el token
        decoded_token = jwt.decode(
            token,
            signing_key,
            algorithms=["RS256"],
            audience=os.environ["CLIENT_ID"]
        )

        print("Acceso permitido a:", decoded_token)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Bienvenido!", "user": decoded_token})
        }

    except jwt.ExpiredSignatureError:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "El token ha expirado"})
        }
    except jwt.InvalidTokenError:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Token inválido"})
        }
