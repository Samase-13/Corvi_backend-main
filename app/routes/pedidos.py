from flask import Blueprint, jsonify, request
from app.models import Pedido, Usuario, Repuestos
from app.extensions import db
from app.utils.token_required import token_required
from datetime import datetime
import json

pedidos_bp = Blueprint('pedidos', __name__, url_prefix='/pedidos')

@pedidos_bp.route('/usuario/<int:id_usuario>', methods=['GET'])
@token_required
def get_pedidos_usuario(id_usuario):
    """Obtener los pedidos de un usuario por su ID."""
    pedidos = Pedido.query.filter_by(id_usuario=id_usuario).all()
    if not pedidos:
        return jsonify({'error': 'No se encontraron pedidos para este usuario'}), 404

    output = []
    for pedido in pedidos:
        productos = json.loads(pedido.productos)
        output.append({
            'id_pedido': pedido.id_pedido,
            'codigo_rastreo': pedido.codigo_rastreo,
            'productos': productos,
            'total': pedido.total,
            'fecha_creacion': pedido.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(output), 200
