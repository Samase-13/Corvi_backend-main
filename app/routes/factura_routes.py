from flask import Blueprint, request, jsonify, send_file
from app.services.factura_service import FacturaService
from io import BytesIO

factura_bp = Blueprint('factura', __name__)
factura_service = FacturaService()

@factura_bp.route('/facturas', methods=['POST'])
def crear_factura():
    data = request.get_json()

    # Validar datos recibidos
    required_fields = ('id_usuario', 'id_maquinaria', 'monto_total', 'archivo_pdf')
    if not all(k in data for k in required_fields):
        return jsonify({'message': 'Faltan datos necesarios'}), 400

    nueva_factura = factura_service.crear_factura(
        id_usuario=data['id_usuario'],
        id_maquinaria=data['id_maquinaria'],
        monto_total=data['monto_total'],
        archivo_pdf=data['archivo_pdf']  # URL del PDF de Firebase
    )

    return jsonify({'message': 'Factura creada', 'id_factura': nueva_factura.id_factura}), 201

@factura_bp.route('/facturas/<int:id_factura>', methods=['GET'])
def obtener_factura(id_factura):
    factura = factura_service.obtener_factura(id_factura)

    if factura:
        return jsonify({
            'id_factura': factura.id_factura,
            'id_usuario': factura.id_usuario,
            'id_maquinaria': factura.id_maquinaria,
            'fecha_emision': factura.fecha_emision.isoformat(),
            'monto_total': factura.monto_total,
            'archivo_pdf': factura.archivo_pdf,
            'estado': factura.estado
        }), 200

    return jsonify({'message': 'Factura no encontrada'}), 404

@factura_bp.route('/facturas/<int:id_factura>/descargar', methods=['GET'])
def descargar_factura(id_factura):
    try:
        pdf_content = factura_service.descargar_pdf(id_factura)
        return send_file(BytesIO(pdf_content), mimetype='application/pdf', as_attachment=True, download_name=f'factura_{id_factura}.pdf')
    except Exception as e:
        return jsonify({'message': str(e)}), 404

@factura_bp.route('/facturas', methods=['GET'])
def listar_facturas():
    facturas = factura_service.listar_facturas()

    return jsonify([{
        'id_factura': factura.id_factura,
        'id_usuario': factura.id_usuario,
        'id_maquinaria': factura.id_maquinaria,
        'fecha_emision': factura.fecha_emision.isoformat(),
        'monto_total': factura.monto_total,
        'archivo_pdf': factura.archivo_pdf,
        'estado': factura.estado
    } for factura in facturas]), 200
