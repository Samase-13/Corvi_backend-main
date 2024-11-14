# app/utils/token_required.py
from functools import wraps
from flask import request, jsonify

# Define el access token que la API espera para autenticación
ACCESS_TOKEN = "APP_USR-7085813680131461-111301-f242d511c1ba522b72195af5369aa2d1-2090063386"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != f'Bearer {ACCESS_TOKEN}':
            return jsonify({'error': 'Token inválido o no proporcionado'}), 403
        return f(*args, **kwargs)
    return decorated
