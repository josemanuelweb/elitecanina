from flask import Flask, render_template, request, redirect, url_for
import mercadopago
import os

app = Flask(__name__)

# CONFIGURACIÓN DE MERCADO PAGO
# En Render usa la variable de entorno. En tu PC, si da error, 
# podés pegar tu token entre las comillas de abajo para probar localmente.
ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN", "TU_TOKEN_DE_PRUEBA_AQUÍ")
sdk = mercadopago.SDK(ACCESS_TOKEN)

# CATÁLOGO REAL DE HAPPY PET (Precios sugeridos con margen)
PRODUCTOS = [
    {
        "id": "1", 
        "nombre": "Pretal con Alitas", 
        "precio": 6500, 
        "img": "alitas.webp", 
        "desc": "Diseño exclusivo y tierno para gatos o perros pequeños. Ajustable y seguro."
    },
    {
        "id": "2", 
        "nombre": "Serpiente Chillona", 
        "precio": 12500, 
        "img": "serpiente.webp", 
        "desc": "Juguete interactivo de gran tamaño con sonido. Estimula el instinto de juego."
    },
    {
        "id": "3", 
        "nombre": "Comedero Doble Cartera", 
        "precio": 25000, 
        "img": "comedero.webp", 
        "desc": "Diseño premium plegable tipo cartera. Ideal para viajes y paseos con estilo."
    },
    {
        "id": "4", 
        "nombre": "Correa de Adiestramiento", 
        "precio": 11000, 
        "img": "correa.webp", 
        "desc": "Correa reforzada de alta resistencia para paseos controlados y seguros."
    },
    {
        "id": "5", 
        "nombre": "Tirador Peluche Flor", 
        "precio": 28500, 
        "img": "peluche.webp", 
        "desc": "Juguete de arrastre premium con texturas suaves y costuras reforzadas."
    },
    {
        "id": "6", 
        "nombre": "Pelota Caucho con Soga", 
        "precio": 7500, 
        "img": "pelota.webp", 
        "desc": "Material ultra resistente. Ideal para juegos de lanzar y recuperar."
    }
]

@app.route('/')
def index():
    return render_template('index.html', productos=PRODUCTOS)

@app.route('/comprar/<id_producto>')
def comprar(id_producto):
    # Buscamos el producto en la lista
    producto = next((p for p in PRODUCTOS if p['id'] == id_producto), None)
    
    if not producto:
        return "Producto no encontrado", 404

    # CREAR PREFERENCIA EN MERCADO PAGO
    preference_data = {
        "items": [
            {
                "title": producto['nombre'],
                "quantity": 1,
                "unit_price": producto['precio'],
            }
        ],
        "back_urls": {
            "success": "https://elitecanina.onrender.com",
            "failure": "https://elitecanina.onrender.com",
            "pending": "https://elitecanina.onrender.com"
        },
        "auto_return": "approved",
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    
    # Redirigir al checkout de Mercado Pago
    return redirect(preference["init_point"])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)