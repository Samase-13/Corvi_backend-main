# app/routes/shipping.py

from flask import Blueprint, request, jsonify
import requests
from app.utils.token_required import token_required, ACCESS_TOKEN

# Crear el Blueprint para la funcionalidad de envíos
shipping_bp = Blueprint('shipping', __name__, url_prefix='/shipping')

# 1. Autorizaciones: Endpoint para autorizar un envío
@shipping_bp.route('/authorize', methods=['POST'])
@token_required
def authorize_envio():
    data = request.json
    # Lógica para enviar autorización al sistema de correo o gestionar la autorización
    return jsonify({'message': 'Autorización de envío realizada'}), 200

# 2. Cancelaciones: Endpoint para cancelar un envío
@shipping_bp.route('/cancel', methods=['PUT'])
@token_required
def cancelar_envio():
    data = request.json
    # Lógica para cancelar el envío tanto en tu sistema como en Mercado Libre
    return jsonify({'message': 'Cancelación de envío exitosa'}), 200

# 3. Registro de Agencias: Endpoint para registrar agencias de envío
@shipping_bp.route('/agencias', methods=['POST'])
@token_required
def registrar_agencia():
    data = request.json
    # Lógica para enviar información de agencias a Mercado Libre o registrarlas en tu sistema
    return jsonify({'message': 'Agencia registrada con éxito'}), 200

# 4. Notificaciones Push Tracking: Enviar actualización de tracking a Mercado Libre
# app/routes/shipping.py

@shipping_bp.route('/tracking/push', methods=['POST'])
@token_required
def enviar_notificacion_tracking():
    data = request.json
    shipment_id = data.get('shipment_id')  # Asegúrate de incluir shipment_id en el JSON de entrada
    tracking_url = f"https://api.mercadolibre.com/shipments/{shipment_id}/tracking"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    response = requests.post(tracking_url, headers=headers, json=data)
    
    if response.status_code == 200:
        return jsonify({'message': 'Notificación de tracking enviada'}), 200
    else:
        print("Error en notificación push tracking:", response.json())
        return jsonify({'error': 'Error en la notificación de tracking'}), 400


# 5. Notificaciones Pull Tracking: Recibir consulta de tracking de Mercado Libre
@shipping_bp.route('/tracking/pull', methods=['POST'])
@token_required
def recibir_notificacion_tracking():
    data = request.json
    # Lógica para recibir y procesar la consulta de tracking desde Mercado Libre
    return jsonify({'message': 'Consulta de tracking recibida'}), 200

# 6. Cálculo de Envío: Costo estimado de envío en Mercado Libre
def calcular_envio(zip_code, peso, alto, ancho, largo):
    shipping_url = f"https://api.mercadolibre.com/sites/MPE/shipping_options?zip_code={zip_code}&dimensions={peso}x{alto}x{ancho}x{largo}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(shipping_url, headers=headers)
    
    if response.status_code == 200:
        shipping_data = response.json()
        # Extrae el costo del primer método de envío disponible
        costo_envio = shipping_data.get('options', [])[0].get('cost', 0)
        return costo_envio
    else:
        print("Error al obtener costo de envío:", response.json())
        return None

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

# 7. Colecta: Endpoint para solicitar la recolección de paquetes
@shipping_bp.route('/colecta', methods=['POST'])
@token_required
def solicitar_colecta():
    data = request.json
    collect_url = "https://api.mercadolibre.com/your_collect_endpoint"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.post(collect_url, headers=headers, json=data)
    
    if response.status_code == 200:
        return jsonify({'message': 'Colecta solicitada con éxito'}), 200
    else:
        print("Error en solicitud de colecta:", response.json())
        return jsonify({'error': 'Error al solicitar colecta'}), 400
