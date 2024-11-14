# app/routes/repuestos.py

from flask import Blueprint, request, jsonify
from app.models import Repuestos
from app import db
import requests
from app.utils.token_required import token_required, ACCESS_TOKEN  # Importa el token

# Crear el Blueprint
bp = Blueprint('repuestos', __name__, url_prefix='/repuestos')

# Función para publicar en Mercado Libre
def publicar_en_mercado_libre(data):
    mercado_libre_url = "https://api.mercadolibre.com/items"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Reemplaza "YOUR_CATEGORY_ID" con el ID de la categoría correcto
    payload = {
    "title": data['nombre'],
    "category_id": "MPE373055",
    "price": data['precio'],
    "currency_id": "PEN",
    "available_quantity": int(data['disponibilidad']),
    "buying_mode": "buy_it_now",
    "listing_type_id": "gold_special",
    "condition": "new",
    "description": {"plain_text": data['descripcion']},
    "pictures": [{"source": data['imagen']}],
    "attributes": [
        {"id": "BRAND", "value_name": data.get('marca', "Sin marca")},
        {"id": "MODEL", "value_name": data.get('modelo', "Modelo desconocido")},
        {"id": "WEIGHT", "value_name": data.get('peso', "Peso desconocido")},
        {"id": "PART_NUMBER", "value_name": data.get('numero_pieza', "Número desconocido")}  # Agrega el número de pieza
    ]
}

    response = requests.post(mercado_libre_url, headers=headers, json=payload)
    
    if response.status_code == 201:
        return response.json()
    else:
        print("Error al publicar en Mercado Libre:", response.json())
        return None


# Crear (POST)
@bp.route('/', methods=['POST'])
@token_required
def add_repuesto():
    data = request.get_json()
    nuevo_repuesto = Repuestos(
        nombre=data['nombre'],
        descripcion=data['descripcion'],
        precio=data['precio'],
        disponibilidad=bool(data['disponibilidad']),
        voltaje=data['voltaje'],
        imagen=data.get('imagen')
    )
    db.session.add(nuevo_repuesto)
    db.session.commit()

    # Publicar en Mercado Libre
    ml_response = publicar_en_mercado_libre(data)
    if ml_response:
        nuevo_repuesto.mercado_libre_id = ml_response['id']
        db.session.commit()

    return jsonify({'message': 'Repuesto agregado con éxito'}), 201

# Leer todos los repuestos (GET)
@bp.route('/', methods=['GET'])
@token_required
def get_repuestos():
    repuestos = Repuestos.query.all()
    output = [
        {
            'id_repuestos': r.id_repuestos,
            'nombre': r.nombre,
            'descripcion': r.descripcion,
            'precio': float(r.precio),
            'disponibilidad': r.disponibilidad,
            'voltaje': float(r.voltaje),
            'imagen': r.imagen
        }
        for r in repuestos
    ]
    return jsonify(output)

# Leer un repuesto por ID (GET)
@bp.route('/<int:id>', methods=['GET'])
@token_required
def get_repuesto(id):
    repuesto = Repuestos.query.get_or_404(id)
    return jsonify({
        'id_repuestos': repuesto.id_repuestos,
        'nombre': repuesto.nombre,
        'descripcion': repuesto.descripcion,
        'precio': repuesto.precio,
        'disponibilidad': repuesto.disponibilidad,
        'voltaje': repuesto.voltaje,
        'imagen': repuesto.imagen
    })

# Actualizar un repuesto (PUT)
@bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_repuesto(id):
    repuesto = Repuestos.query.get_or_404(id)
    data = request.get_json()

    repuesto.nombre = data.get('nombre', repuesto.nombre)
    repuesto.descripcion = data.get('descripcion', repuesto.descripcion)
    repuesto.precio = data.get('precio', repuesto.precio)
    repuesto.disponibilidad = data.get('disponibilidad', repuesto.disponibilidad)
    repuesto.voltaje = data.get('voltaje', repuesto.voltaje)
    repuesto.imagen = data.get('imagen', repuesto.imagen)

    db.session.commit()
    return jsonify({'message': 'Repuesto actualizado con éxito'})

# Eliminar un repuesto (DELETE)
@bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_repuesto(id):
    repuesto = Repuestos.query.get_or_404(id)
    db.session.delete(repuesto)
    db.session.commit()
    return jsonify({'message': 'Repuesto eliminado con éxito'})