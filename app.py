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
        "nombre": "Masajeador Facial Ultrasónico", 
        "precio": 24500, 
        "img": "ultrasonico.webp", 
        "desc": "Tecnología de iones para rejuvenecimiento facial y limpieza profunda."
        },
    {
        "id": "2", 
        "nombre": "Succionador de Poros Digital", 
        "precio": 21000, 
        "img": "succionador.webp", 
        "desc": "Elimina puntos negros con 5 niveles de succión y pantalla LED."
        },
    {
        "id": "3", 
        "nombre": "Máscara LED Facial 7 Colores", 
        "precio": 45000, 
        "img": "mascara.webp", 
        "desc": "Tratamiento de fototerapia profesional para manchas y arrugas."
        },
    {
        "id": "4", 
        "nombre": "Depilador Facial LED Pro", 
        "precio": 15500, 
        "img": "depilador.webp", 
        "desc": "Remoción de vello facial sin dolor, compacto y recargable USB."
        },
    {
        "id": "5", 
        "nombre": "Kit Gua Sha Cuarzo Rosa", 
        "precio": 18900, 
        "img": "guasha.webp", 
        "desc": "Piedra natural para drenaje linfático y definición del rostro."
        },
    {
        "id": "6", 
        "nombre": "Cepillo Limpiador Silicona", 
        "precio": 12500, 
        "img": "cepillo.webp", 
        "desc": "Vibración sónica para una limpieza profunda y masaje facial."
    }
]

@app.route('/')
def index():
    return render_template('index.html', productos=PRODUCTOS)

@app.route('/comprar/<id_producto>')
def comprar(id_producto):
    producto = next((p for p in PRODUCTOS if p['id'] == id_producto), None)
    if not producto:
        return "Producto no encontrado", 404

    # Creamos el mensaje para WhatsApp
    mensaje = f"Hola Elite Canina! Me interesa comprar el producto: {producto['nombre']}"
    # Codificamos el mensaje para que funcione en un link (reemplaza espacios por %20)
    import urllib.parse
    mensaje_codificado = urllib.parse.quote(mensaje)
    
    # Redirigimos directamente al WhatsApp con el mensaje personalizado
    # Reemplaza el número por el tuyo
    return redirect(f"https://wa.me/5491125427382?text={mensaje_codificado}")

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    
    # Redirigir al checkout de Mercado Pago
    return redirect(preference["init_point"])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)