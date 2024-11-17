from flask import Blueprint, jsonify, request
from app.models import Pedido, Usuario, Envio
from app.extensions import db
import requests
import json
from datetime import datetime
from app.utils.token_required import token_required, ACCESS_TOKEN

mercado_pago_bp = Blueprint("mercado_pago", __name__)

@mercado_pago_bp.route("/pago", methods=["POST"])
@token_required
def realizar_pago():
    # Obtener datos del carrito y usuario
    data = request.get_json()
    id_usuario = data.get('id_usuario')
    productos = data.get('productos', [])
    total = sum(item['quantity'] * item['unit_price'] for item in productos)

    # Validar usuario
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Generar código de rastreo
    codigo_rastreo = f"CR{int(datetime.utcnow().timestamp())}"

    # Crear preferencia en Mercado Pago
    url = "https://api.mercadopago.com/checkout/preferences"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}',
    }

    preference_data = {
        "items": [
            {
                "title": item['title'],
                "quantity": item['quantity'],
                "unit_price": item['unit_price'],
                "currency_id": "PEN"
            }
            for item in productos
        ],
        "payer": {
            "name": usuario.nombre,
            "email": usuario.correo
        },
        "back_urls": {
            "success": "https://miweb.com/pago-exitoso",
            "failure": "https://miweb.com/pago-fallido",
            "pending": "https://miweb.com/pago-pendiente"
        },
        "auto_return": "approved"
    }

    response = requests.post(url, json=preference_data, headers=headers)
    if response.status_code != 201:
        return jsonify({"error": "Error al generar el enlace de pago", "details": response.json()}), 500

    payment_url = response.json().get("init_point")

    # Registrar pedido y envío en la base de datos
    try:
        nuevo_pedido = Pedido(
            id_usuario=id_usuario,
            codigo_rastreo=codigo_rastreo,
            productos=json.dumps(productos),
            total=total
        )
        db.session.add(nuevo_pedido)

        nuevo_envio = Envio(
            codigo_rastreo=codigo_rastreo,
            destino=data.get('destino', 'Sin destino')
        )
        db.session.add(nuevo_envio)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al registrar el pedido", "details": str(e)}), 500

    return jsonify({"payment_url": payment_url}), 200
