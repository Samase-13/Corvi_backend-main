from app import db
from datetime import datetime

class Repuestos(db.Model):
    __tablename__ = 'repuestos'
    id_repuestos = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    disponibilidad = db.Column(db.String(50), nullable=False)
    voltaje = db.Column(db.Numeric(10, 2), nullable=False)
    imagen = db.Column(db.String(200), nullable=True)
    
    def __repr__(self):
        return f'<Repuestos {self.nombre}>'

class Maquinaria(db.Model):
    __tablename__ = 'maquinaria'
    id_maquinaria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String(200), nullable=True)
    precio_hora = db.Column(db.Numeric(10, 2), nullable=False)  # Precio por hora
    precio_dia = db.Column(db.Numeric(10, 2), nullable=False)   # Precio por día
    descripcion = db.Column(db.Text, nullable=True)
    
    # Nuevo campo estado que solo admite 'disponible' o 'ocupado'
    estado = db.Column(db.Enum('disponible', 'ocupado', name='estado_maquinaria'), nullable=False, default='disponible')

    # Relación uno a muchos con el calendario de disponibilidad
    disponibilidad_calendario = db.relationship('DisponibilidadCalendario', backref='maquinaria', lazy=True)

    def __repr__(self):
        return f'<Maquinaria {self.nombre}>'


class DisponibilidadCalendario(db.Model):
    __tablename__ = 'disponibilidad_calendario'
    id_disponibilidad = db.Column(db.Integer, primary_key=True)
    id_maquinaria = db.Column(db.Integer, db.ForeignKey('maquinaria.id_maquinaria'), nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=True)
    fecha_fin = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Disponibilidad {self.id_disponibilidad} para Maquinaria {self.id_maquinaria}>'

class Factura(db.Model):
    __tablename__ = 'facturas'
    id_factura = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)  # Asumiendo que tienes una tabla de usuarios
    id_maquinaria = db.Column(db.Integer, db.ForeignKey('maquinaria.id_maquinaria'), nullable=False)  # Si la factura está asociada a una maquinaria
    fecha_emision = db.Column(db.DateTime, nullable=False)  # Fecha de emisión de la factura
    monto_total = db.Column(db.Float, nullable=False)  # Monto total de la factura
    archivo_pdf = db.Column(db.String(200), nullable=False)  # Ruta del archivo PDF almacenado
    estado = db.Column(db.Enum('pagada', 'pendiente', 'cancelada', name='estado_factura'), nullable=False, default='pendiente')

    # Relación inversa si es necesario
    usuario = db.relationship('Usuario', backref='facturas', lazy=True)  # Asegúrate de tener un modelo Usuario

    def __repr__(self):
        return f'<Factura {self.id_factura}, Usuario {self.id_usuario}, Monto {self.monto_total}>'

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    dni = db.Column(db.String(8), unique=True, nullable=False)  # Suponiendo que el DNI tiene 8 dígitos
    # Puedes añadir otros campos que consideres necesarios

    def __repr__(self):
        return f'<Usuario {self.nombre}, DNI {self.dni}>'
class Envio(db.Model):
    __tablename__ = 'envios'
    id_envio = db.Column(db.Integer, primary_key=True)
    codigo_rastreo = db.Column(db.String(100), unique=True, nullable=False)
    estado = db.Column(db.String(50), nullable=False, default='En preparación')
    destino = db.Column(db.String(255), nullable=False)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Envio {self.codigo_rastreo}>'

class HistorialEnvio(db.Model):
    __tablename__ = 'historial_envios'
    id_historial = db.Column(db.Integer, primary_key=True)
    id_envio = db.Column(db.Integer, db.ForeignKey('envios.id_envio'), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    observaciones = db.Column(db.Text, nullable=True)

    envio = db.relationship('Envio', backref='historial')

    def __repr__(self):
        return f'<Historial {self.id_historial} - Estado: {self.estado}>'

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id_pedido = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    codigo_rastreo = db.Column(db.String(50), nullable=False, unique=True)
    productos = db.Column(db.Text, nullable=False)  # Se guardarán como JSON
    total = db.Column(db.Float, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('Usuario', backref='pedidos', lazy=True)

    def __repr__(self):
        return f'<Pedido {self.id_pedido}, Usuario {self.id_usuario}, Total {self.total}>'
