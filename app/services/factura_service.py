# factura_service.py
from app.models import Factura  # Asegúrate de que esta importación sea correcta
from app import db
from datetime import datetime
import requests

class FacturaService:
    def crear_factura(self, id_usuario, id_maquinaria, monto_total, archivo_pdf):
        nueva_factura = Factura(
            id_usuario=id_usuario,
            id_maquinaria=id_maquinaria,
            fecha_emision=datetime.utcnow(),  # Asigna la fecha actual
            monto_total=monto_total,
            archivo_pdf=archivo_pdf,
            estado='pendiente'  # Estado por defecto
        )
        db.session.add(nueva_factura)
        db.session.commit()
        return nueva_factura

    def obtener_factura(self, id_factura):
        return Factura.query.get(id_factura)

    def listar_facturas(self):
        return Factura.query.all()

    def descargar_pdf(self, id_factura):
        factura = self.obtener_factura(id_factura)
        if factura:
            pdf_url = factura.archivo_pdf
            response = requests.get(pdf_url)
            if response.status_code == 200:
                return response.content  # Retorna el contenido del PDF
            else:
                raise Exception("Error al obtener el PDF: " + response.reason)
        else:
            raise Exception("Factura no encontrada.")
