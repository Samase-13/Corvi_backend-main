from app import db
from app.models import Pedido, Repuestos, Usuario
from datetime import datetime

class PedidoService:
    @staticmethod
    def crear_pedido(data):
        # Validar datos recibidos
        if 'id_usuario' not in data or 'id_repuesto' not in data or 'cantidad' not in data or 'direccion_envio' not in data or 'metodo_envio' not in data or 'costo_envio' not in data or 'monto_total' not in data:
            raise ValueError("Datos incompletos")

        # Verificar que el usuario y el repuesto existen
        usuario = Usuario.query.get(data['id_usuario'])
        repuesto = Repuestos.query.get(data['id_repuesto'])

        if not usuario or not repuesto:
            raise ValueError("Usuario o repuesto no encontrado")

        # Crear el nuevo pedido
        nuevo_pedido = Pedido(
            id_usuario=data['id_usuario'],
            id_repuesto=data['id_repuesto'],
            cantidad=data['cantidad'],
            direccion_envio=data['direccion_envio'],
            metodo_envio=data['metodo_envio'],
            costo_envio=data['costo_envio'],
            monto_total=data['monto_total'],  # Asegúrate de que esto esté incluido en tu data
            fecha_creacion=datetime.utcnow()  # O la fecha que desees
        )

        db.session.add(nuevo_pedido)
        db.session.commit()
        return nuevo_pedido.id_pedido

    @staticmethod
    def obtener_pedido(id_pedido):
        pedido = Pedido.query.get(id_pedido)
        if not pedido:
            raise ValueError("Pedido no encontrado")
        return pedido

    @staticmethod
    def listar_pedidos():
        return Pedido.query.all()

    @staticmethod
    def eliminar_pedido(id_pedido):
        pedido = Pedido.query.get(id_pedido)
        if not pedido:
            raise ValueError("Pedido no encontrado")
        db.session.delete(pedido)
        db.session.commit()
