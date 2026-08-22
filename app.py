import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, session, render_template

from db import obtener_conexion
from utils.formatear_texto import formatear_texto
from utils.es_video import es_video
from utils.youtube_embed_url import youtube_embed_url
from utils.google_maps_embed_url import google_maps_embed_url
from utils.whatsapp_numero import whatsapp_numero
from utils.formatear_fecha import formatear_fecha
from utils.clase_area import clase_area

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret')

# Equivalente a app.locals en Express: funciones disponibles en todas las plantillas
app.jinja_env.globals['formatearTexto'] = formatear_texto
app.jinja_env.globals['esVideo'] = es_video
app.jinja_env.globals['youtubeEmbedUrl'] = youtube_embed_url
app.jinja_env.globals['googleMapsEmbedUrl'] = google_maps_embed_url
app.jinja_env.globals['whatsappNumero'] = whatsapp_numero
app.jinja_env.globals['formatearFecha'] = formatear_fecha
app.jinja_env.globals['claseArea'] = clase_area


@app.context_processor
def inyectar_datos_globales():
    """Equivalente a los middlewares de app.js que ponen 'usuario' y 'sitio/contacto'
    disponibles en todas las plantillas, en cada request."""
    usuario = session.get('usuario')

    sitio = {}
    try:
        with obtener_conexion() as conexion:
            with conexion.cursor() as cur:
                cur.execute('SELECT * FROM institucion_info ORDER BY id LIMIT 1')
                fila = cur.fetchone()
                sitio = fila or {}
    except Exception as err:
        print('No se pudo cargar institucion_info:', err)
        sitio = {}

    return {'usuario': usuario, 'sitio': sitio, 'contacto': sitio, 'anio_actual': datetime.now().year}


# --- Blueprints (rutas) ---
from blueprints.public import public_bp
from blueprints.auth import auth_bp
from blueprints.admin import admin_bp
app.register_blueprint(public_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html', titulo='Pagina no encontrada'), 404


if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=puerto, debug=True)
