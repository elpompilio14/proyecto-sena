from flask import Blueprint, render_template
from db import obtener_conexion

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def home():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cur:
            cur.execute('SELECT * FROM eventos ORDER BY fecha DESC LIMIT 6')
            eventos = cur.fetchall()

            cur.execute('SELECT * FROM noticias ORDER BY fecha DESC LIMIT 3')
            noticias = cur.fetchall()

            cur.execute('SELECT himno_url, fondo_url FROM institucion_info ORDER BY id LIMIT 1')
            info = cur.fetchone()

    return render_template(
        'home.html',
        titulo='Inicio',
        eventos=eventos,
        noticias=noticias,
        himnoUrl=info['himno_url'] if info else None,
        fondoUrl=info['fondo_url'] if info else None,
    )
