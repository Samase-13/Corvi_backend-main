from app import create_app
from flask_cors import CORS

app = create_app()

# Habilitar CORS para todas las rutas
CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)