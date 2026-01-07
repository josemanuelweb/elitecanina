from flask import Flask, render_template, redirect, url_for
import os
import mercadopago

app = Flask(__name__)

# Configuración de Mercado Pago (Usa tu Access Token de prueba primero)
# Conseguilo en: https://developers.mercadopago.com.ar/panel
sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))

# Base de datos simulada (Luego la podés pasar a SQL)
PRODUCTOS = [
    {
        "id": "1",
        "nombre": "Arnés Elite Pro Tactical",
        "precio": 38500,
        "img": "arnes.jpg",
        "desc": "Control total y confort para paseos urbanos."
    },
    {
        "id": "2",
        "nombre": "Cama Anti-Stress Nube",
        "precio": 42000,
        "img": "cama.jpeg",
        "desc": "Diseño ortopédico para un descanso profundo."
    },
    {
        "id": "1",
        "nombre": "Arnés Elite Pro Tactical",
        "precio": 38500,
        "img": "arnes.jpg",
        "desc": "Control total y confort para paseos urbanos."
    },
    {
        "id": "2",
        "nombre": "Cama Anti-Stress Nube",
        "precio": 42000,
        "img": "cama.jpeg",
        "desc": "Diseño ortopédico para un descanso profundo."
    }
]

@app.route('/')
def index():
    # Aquí es donde ocurre el enlace:
    # 'productos' (en minúsculas) es el nombre que usará el HTML
    # 'PRODUCTOS' (en mayúsculas) es la lista que creaste arriba
    return render_template('index.html', productos=PRODUCTOS)

@app.route('/comprar/<id_producto>')
def comprar(id_producto):
    # Buscar el producto seleccionado
    producto = next((p for p in PRODUCTOS if p['id'] == id_producto), None)
    
    if not producto:
        return "Producto no encontrado", 404

    # Crear preferencia en Mercado Pago
    preference_data = {
        "items": [
            {
                "title": producto['nombre'],
                "quantity": 1,
                "unit_price": producto['precio'],
                "currency_id": "ARS"
            }
        ],
        "back_urls": {
            "success": "http://127.0.0.1:5000/exito",
            "failure": "http://127.0.0.1:5000/",
            "pending": "http://127.0.0.1:5000/"
        },
        "auto_return": "approved",
    }

    preference_response = sdk.preference().create(preference_data)
    url_pago = preference_response["response"]["init_point"]
    
    return redirect(url_pago)

@app.route('/exito')
def exito():
    return render_template('success.html')

if __name__ == "__main__":
    # Render asigna un puerto automáticamente, esto lo captura:
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)