from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:lester.com@localhost/corvi_bd'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Importar modelos antes de crear las tablas
    from .models import Usuario, Factura  # Esto es necesario

    # Registrar blueprints
    from .routes import repuestos, maquinaria, disponibilidad, ruc, factura_routes, usuario_routes
    app.register_blueprint(repuestos.bp)
    app.register_blueprint(maquinaria.bp)
    app.register_blueprint(disponibilidad.bp)
    app.register_blueprint(ruc.ruc_bp)
    app.register_blueprint(factura_routes.factura_bp)
    app.register_blueprint(usuario_routes.usuario_bp)
    
    with app.app_context():
        db.create_all()  # Crea todas las tablas si no existen

    return app
