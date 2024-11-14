# app/utils/api_utils.py
import requests
from flask import jsonify

def make_request(url, headers, data=None):
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return jsonify({"error": "Error en la solicitud a Mercado Libre", "details": str(http_err)}), 400
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        return jsonify({"error": "Error de conexión con Mercado Libre"}), 503
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        return jsonify({"error": "Tiempo de espera excedido en la solicitud a Mercado Libre"}), 504
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
        return jsonify({"error": "Error desconocido en la solicitud a Mercado Libre"}), 500
