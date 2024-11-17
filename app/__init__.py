# app/__init__.py
from flask import Flask
from app.extensions import db, migrate
from app.routes.repuestos import bp as repuestos_bp
from app.routes.shipping import shipping_bp  # Importa el blueprint correcto
from app.routes.mercadopago import mercado_pago_bp
from app.routes.tracking import tracking_bp
from app.routes.pedidos import pedidos_bp

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:lester.com@localhost/corvi_bd'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar las extensiones
    db.init_app(app)
    migrate.init_app(app, db)  # Conectar Flask-Migrate a la aplicación y a la base de datos

    # Importar modelos dentro del contexto de la aplicación para evitar imports circulares
    with app.app_context():
        from .models import Usuario, Factura, Repuestos, Maquinaria, DisponibilidadCalendario, Envio, HistorialEnvio, Pedido

    # Registrar blueprints
    from .routes import repuestos, maquinaria, disponibilidad, ruc, factura_routes, usuario_routes
    app.register_blueprint(repuestos.bp)
    app.register_blueprint(maquinaria.bp)
    app.register_blueprint(disponibilidad.bp)
    app.register_blueprint(ruc.ruc_bp)
    app.register_blueprint(factura_routes.factura_bp)
    app.register_blueprint(usuario_routes.usuario_bp)
    app.register_blueprint(shipping_bp, url_prefix='/shipping')
    app.register_blueprint(mercado_pago_bp, url_prefix='/mercado_pago')
    app.register_blueprint(tracking_bp, url_prefix='/tracking')
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')


    # Crear tablas si no existen
    with app.app_context():
        db.create_all()

    return app
