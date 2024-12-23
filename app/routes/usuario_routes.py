from flask import Blueprint, request, jsonify
from app.services.usuario_service import UsuarioService
from app.models import Usuario
from app import db

usuario_bp = Blueprint('usuario', __name__)
usuario_service = UsuarioService()

@usuario_bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    try:
        nuevo_usuario = usuario_service.crear_usuario(
            nombre=data['nombre'],
            correo=data['correo'],
            dni=data['dni']
        )
        return jsonify({'message': 'Usuario creado', 'id_usuario': nuevo_usuario.id_usuario}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@usuario_bp.route('/usuarios/<int:id_usuario>', methods=['GET'])
def obtener_usuario(id_usuario):
    usuario = usuario_service.obtener_usuario(id_usuario)
    if usuario:
        return jsonify({
            'id_usuario': usuario.id_usuario,
            'nombre': usuario.nombre,
            'correo': usuario.correo,
            'dni': usuario.dni
        })
    return jsonify({'message': 'Usuario no encontrado'}), 404

@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = usuario_service.listar_usuarios()
    return jsonify([
        {
            'id_usuario': usuario.id_usuario,
            'nombre': usuario.nombre,
            'correo': usuario.correo,
            'dni': usuario.dni
        }
        for usuario in usuarios
    ])
    
@usuario_bp.route('/usuarios/<int:id_usuario>/pedidos', methods=['GET'])
def obtener_pedidos(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    pedidos = Pedido.query.filter_by(id_usuario=id_usuario).all()
    pedidos_data = [
        {
            'id_pedido': pedido.id_pedido,
            'codigo_rastreo': pedido.codigo_rastreo,
            'productos': json.loads(pedido.productos),
            'total': pedido.total,
            'fecha_creacion': pedido.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')
        }
        for pedido in pedidos
    ]
    return jsonify(pedidos_data), 200
