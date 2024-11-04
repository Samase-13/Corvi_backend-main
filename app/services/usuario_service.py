# usuario_service.py
from app.models import Usuario  # Corrige esta línea
from app import db

class UsuarioService:
    def crear_usuario(self, nombre, correo, dni):
        nuevo_usuario = Usuario(
            nombre=nombre,
            correo=correo,
            dni=dni
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return nuevo_usuario

    def obtener_usuario(self, id_usuario):
        return Usuario.query.get(id_usuario)        

    def listar_usuarios(self):
        return Usuario.query.all()
