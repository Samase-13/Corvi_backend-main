# app/routes/shipping.py

from flask import Blueprint, request, jsonify
import requests
from app.utils.token_required import token_required, ACCESS_TOKEN  # Importa el token

# Crear el Blueprint para los envíos
shipping_bp = Blueprint('shipping', __name__, url_prefix='/shipping')

# Función para calcular el costo de envío en Mercado Libre
def calcular_envio(zip_code, peso, alto, ancho, largo):
    shipping_url = f"https://api.mercadolibre.com/sites/MPE/shipping_options?zip_code={zip_code}&dimensions={peso}x{alto}x{ancho}x{largo}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    response = requests.get(shipping_url, headers=headers)
    
    if response.status_code == 200:
        shipping_data = response.json()
        # Extrae el costo del primer método de envío disponible
        costo_envio = shipping_data.get('options', [])[0].get('cost', 0)  # Modifica si el formato de respuesta es diferente
        return costo_envio
    else:
        print("Error al obtener costo de envío:", response.json())
        return None

# Endpoint para calcular el costo de envío
@shipping_bp.route('/calculate', methods=['POST'])
@token_required
def calcular_costo_envio_producto():
    data = request.get_json()
    zip_code = data['zip_code']
    peso = data['peso']
    alto = data['alto']
    ancho = data['ancho']
    largo = data['largo']

    # Calcula el envío
    costo_envio = calcular_envio(zip_code, peso, alto, ancho, largo)
    
    if costo_envio is not None:
        return jsonify({'costo_envio': costo_envio})
    else:
        return jsonify({'error': 'No se pudo calcular el costo de envío'}), 400
