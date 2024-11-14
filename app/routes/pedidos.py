from flask import Blueprint, request, jsonify
from app.services.pedidos_service import PedidoService

bp = Blueprint('pedidos', __name__)

@bp.route('/pedidos', methods=['POST'])
def crear_pedido_route():
    data = request.get_json()
    try:
        nuevo_pedido_id = PedidoService.crear_pedido(data)
        return jsonify({"id_pedido": nuevo_pedido_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/pedidos/<int:id_pedido>', methods=['GET'])
def obtener_pedido_route(id_pedido):
    try:
        pedido = PedidoService.obtener_pedido(id_pedido)
        return jsonify(pedido), 200  # Asegúrate de serializar el pedido correctamente
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@bp.route('/pedidos', methods=['GET'])
def listar_pedidos_route():
    pedidos = PedidoService.listar_pedidos()
    return jsonify(pedidos), 200  # Asegúrate de serializar la lista de pedidos

@bp.route('/pedidos/<int:id_pedido>', methods=['DELETE'])
def eliminar_pedido_route(id_pedido):
    try:
        PedidoService.eliminar_pedido(id_pedido)
        return jsonify({"message": "Pedido eliminado"}), 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
